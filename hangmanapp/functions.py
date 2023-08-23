# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from django.core.exceptions import ObjectDoesNotExist
from random import randint
from django.db.models import Sum
import requests
from .models import *

# In case everything fails, these words are a back up word dictionary that will infer there was a problem.
fail_safe = [
    "mistake", "fault", "failure", "miscue", "problem", 
    "problematic", "error", "erroneous", "misread", "flopped", 
    "disaster", "disastrous", "catastrophe", "catastrophic",
    "debacle", "tragic", "tragedy", "fiasco", "shambles" 
]


def get_word(user):
    """
    This is where the story starts for creating a word for the hangman round.
    Important comments from development time have not been suppressed.
    Generally, the application should resume any incomplete game (round).
    This can happen if the player leaves the site before either winning
    or losing that round. To do this, the function should first
    query the use history model for complete == False.
    If there is such a case, the word is returned to the application.
    If all words in the user's history are complete, then a new word is generated by
    one of three ways. API, fallback dictionary, or fail_safe local dictionary.
    When a new user first joins and plays, they will have no initial history.
    this will produce an error for the data base model query. If this happens,
    the application will still obtain a word from one of the three methods,
    but will send an empty query list along instead of an error. This means any
    word that has passed the censor will end up in the final list.
    """
    # First, try to get an incomplete word from the DB.
    # Get the list of user words already in DB, order by reversed id.
    if query_list := UserWordHistory.objects.filter(user = user).order_by("-id"):
        if query_list.first().complete == False:
            # The top word is incomplete in the DB.
            # This goes back to the program, now. Done.
            return query_list.first()
        else:
            # Otherwise, complicated stuff starts here...
            # No need to check if the list exists here. Already done above.
            # Here is a list of the last words in the DB for the user.
            # Note, the first word in the list is the last word in the DB.
            # Remember, the id is in reverse order.
            # This slice should ensure that the user does not see a repeat of a word for 40 rounds.
            return primary_get_word_sequence(user, query_list[:40])
    else:
        print("No list")
        return primary_get_word_sequence(user, [])



def primary_get_word_sequence(user, lq_list):
    """
    A reasonably critical function. Here is what happens.
    1. Check if the API returns a list of words.
    2. If the API fails, check if the the fallback dictionary returns a words.
    3. If all that fails, get a word from the local fail safe word list.
    4. If everything fails, return False. There is a big problem.
    """
    if API_words_sample := get_API_words(lq_list):
        print("Got word from API")
        if word_struct := format_entry(user, API_words_sample[randint(0, len(API_words_sample) - 1)]):
            return word_struct
    elif fallback_words_sample := fallback_data_word(lq_list):
        print("Got word from fall back dictionary")
        if word_struct := format_entry(user, fallback_words_sample[randint(0, len(fallback_words_sample) - 1)]):
            return word_struct
    else:
        print("Got word from fail safe")
        if word_struct := format_entry(user, fail_safe[randint(0, len(fail_safe) - 1)]):
            return word_struct
    return False



def get_API_words(lq_list):
    """
    This function uses Pythons own requests module to query a remote word generator API.
    It attempts recover a number of words from this API. If there are any errors,
    it will return None (interpretation as False for the calling function, primary_get_word_sequence).
    """
    try:
        response = requests.get("https://random-word-api.vercel.app/api?words=20")
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return None
    except requests.exceptions.Timeout:
        print("Timeout Error")
        return None
    except requests.exceptions.HTTPError:
        print("HTTP Error")
        return None
    except requests.exceptions.RequestException:
        print("Request Error")
        return None
    except Exception:
        print("Unknown Error")
        return None
    else:    
        # return response.json()
        try:
            # Put the API words through the censor, and return the remainder.
            return censor_API_words(response.json(), lq_list)
        except (OSError, IndexError) as error:
            print(f"ERROR: {error}")
            # If there are any errors from the censor, just return None to acces the fallback mode.
            return None




def censor_API_words(word_list, lq_list):
    """
    This function purges the list of words obtained from the API of any inappropriate words.
    The censor.txt is located in wordbank, and contains a list of words that are not
    really desirable in a hangman game. In the event that the API provides a word that is
    unacceptable, it will be removed from the list. 
    In addition to that, it will also ensure that all the words in the API list are at least
    five letters long.
    The list comprehension will structure a new list containing all the words that were
    not rejected and return that.
    If, for any reason, all words are rejected and an empty list is produced,
    the function will produce an index error. This error is caught up in the Get_API_words
    function.
    """
    try:
        with open("wordbank/censor.txt", "r") as censor_file:
            try:
                censor_list = censor_file.read().split(" ")
            except Exception as io_error:
                print(f"Error reading file: {io_error}")
                raise OSError
            else:
                # Uhm. Turned into a bit of a major list comprehension.
                censored_words = [word for word in word_list if word not in censor_list and word not in lq_list and len(word) > 4]
                # What happens if the censor eliminated all the words?
                if len(censored_words) > 0:
                    return censored_words
                else:
                    print("Error in API Censor, all elements were suppressed.")
                    raise IndexError
    except Exception as file_error:
        print(f"Error opening file: {file_error}")
        raise OSError


def fallback_data_word(lq_list):
    """
    If the word API response has failed, this function recovers a word from a local text file
    that contains a list of words that can be used in the application to play hangman.
    There is no need to censor this file, as it is practically guaranteed not to contain
    inapproriate words.
    Additionally, all words in this file will be longer than 4 words, so there
    is no need to include that condition in the list comprehension,
    as there was in the API recovery method (where many words might be
    four letters long or less).
    lq_list is a list of words from the DB that the user has already solved.
    It is checked here in the list comprehension so that the user will not have
    to (too frequently) run the risk of getting repeat words too soon.
    """
    try:
        with open("wordbank/nouns_en.txt", "r") as fallback_file:
            try:
                fallback_word_list = fallback_file.read().split(" ")
            except Exception as io_error:
                print(f"Error reading file: {io_error}")
                return False
            else:
                fallback_sample_list =  [word for word in fallback_word_list if word not in lq_list]
                if len(fallback_sample_list) > 0:
                    return fallback_sample_list
                else:
                    return fail_safe
                
    except Exception as file_error:
        print(f"Error opening file: {file_error}")
        return False
    

def format_entry(user, word):
    """
    This function writes a new word to the user's word history model,
    when the word is retrieved for the first time.
    It should work normally without problems, main reason for failure being
    unmigrated or altered model in models.py.
    If this does fail, it is a serious problem for the application,
    and the server should be brought down to fix the issues in model.py.
    """
    try:
        new_DB_word = UserWordHistory.objects.create(
            user = user,
            word = word,
            player_word = "_" * len(word),
            used_letters = ""
        )
    except Exception as error:
        print(f"ERROR: Not kidding. Big DB error: {error}\nBring the server down and see what is happening.")
        return False
    else:
        return new_DB_word


def put_score(user):
    """
    Some notes on this function. 
    The very first... this function used to be a view of its own, with a URL, over in views.py.
    However, it was an ineffiecient reuse of a function that was already called in
    game.js. It was better (I think) to avoid a double call to the same function in a loop cycle,
    so this is now conditionally called from the put_history function IF the word is complete.
    ---
    This is called as a result of (via) a fetch request from JavaScript frontend.
    It is paramount that this be called AFTER the word history has been posted for the round.
    Any funny score results, ever, the first thing to check is that this order was not
    accidentally altered. Look in the game.js JavaScript file, for that.
    Almost worth making another fetch block over in the JavaScript game.js, but
    I weigh up the following. wObj is not used here, but is passed, anyway. Wasted effort.
    On the other hand, adding another function in JavaScript injects more
    probability of bugs and errors by lengthening the code. Therefore,
    I opt for the latter, as those two points (bugs and long code) outweigh the wasted shot of reuse.
    ---
    Filtering only the won == true words to get the win_efficiency.
    CAUTION. There is always the possibility that a user has not won any word, yet. This will undoubtedly
    cause a foreseeable problem, as in that case won words will return a count of 0. 
    Any operations on this query set will return None. This is an exception that will need to be handled. 
    Check the queryset count. If it is 0 bypass the calculation for ratio and efficiency. 
    ---
    A risk of division by zero? Should not happen. This procedure is called after the word history
    database is updated, so even if it is the user's first word in their history, all_words should 
    be at least 1 by the time we get here. Any division by zero problems, or strange None errors,
    look here, or check the order of calling in game.js, as mentioned above.
    ---
    There are two Django options for getting counts. Both are useful, and indeed,
    each would have their use for specific cases:
    -
    user_word_records.filter(won = True).aggregate(Count("word"))["word__count"]
    -
    or...
    -
    user_word_records.count()
    -
    The aggregate method has quite a specific use, where .count() is a quick general method.
    Note, aggregate actually singles out a specific attribute in the model. Useful.
    Look carefully at the aggregate method, however.
    Using aggregate. It returns a dict object, rather curiously, and not the number.
    The key to the value is the attribute with a dunder and the operation done, lowercase.
    Weird, but there you go. It is immediately accessible in a one-liner.
    """
    try:
        score_DB = UserScoreCard.objects.get(user = user)
        user_word_records = UserWordHistory.objects.filter(user = user)
        user_won_records = user_word_records.filter(won = True) # Returns a queryset, regardless if empty.
        score_DB.word_count = user_word_records.count() # That is, all_words count
        score_DB.won_count = user_won_records.count() # Only won words.
                
        # if all_won.count() != 0:
        if score_DB.won_count != 0:
            # Suppressed this from the model...
            score_DB.win_ratio = round((score_DB.won_count / score_DB.word_count) * 100)
            win_hits = user_won_records.aggregate(Sum("hits"))["hits__sum"]
            win_misses = user_won_records.aggregate(Sum("misses"))["misses__sum"]
            score_DB.win_efficiency = round((win_hits / (win_hits + win_misses)) * 100)
        else:
            score_DB.win_ratio = 0
            score_DB.win_efficiency = 0

        score_DB.save()
        return True
    
    except Exception as error:
        print(f"ERROR: {error}")
        return False



def home_scores(current_app_user):
    score_pairs = {
        "Expert": (501, 150000), 
        "Addicted": (251, 500), 
        "Dedicated": (51, 250), 
        "Interested": (11, 51), 
        "Sampler": (0, 10)
    }
    # Leaderboard data.
    score_records = UserScoreCard.objects.all().order_by("-win_ratio", "-won_count", "-win_efficiency")
    
    # print(score_records[0].user.username)
    qlist = list()
    level_list = list()
    inner_data = dict()
    current_user_record = None
    # current_user_data default, in case no one is logged in.
    current_user_data = {
        "level": None,
        "place": 0,
        "win_ratio": 0,
        "win_eff": 0
    }
    """
    Okay, what is this next bit doing?
    First, a loop is being established that iterates through each level found in the
    score_pairs keys.
    A score_category is created for the level, which is nothing more than all the records
    filtered by being between (inclusive) the values in the tuple for that level, taken from score records,
    which is everything in the UserScoreCards model.
    Immediately, before anymore iteration is done, it is determined if the current user is in that
    score_category range (this is for the information box on the home.html page of the site).
    Check if the user (logged in, of course) happens to be in that score category.
    If so, user data is collected. Otherwise, default remains.
    Then, the first three items of the queryset for each level are collected in a temporary dict
    called qlist, which itself is made up of three other temporary dicts called inner_data.
    If there are not three places for a particular level (that is, there may not be 3 elements in
    the queryset for that level), the loop to create inner_data will insert blank data instead of 
    producing an index error. 
    Finally, all of this is collected in context dict, and shunted on to the home.html page.
    It is quite a lot to put in the views.py file, so I will probably port this out to functions.py, 
    and return the data as a tuple of dicts to only be unpacked (t)here.
    """
    # Only get the user record if someone is logged in.
    if current_app_user.is_authenticated:
        current_user_record = score_records.get(user = current_app_user)

    for level in score_pairs.keys():
        score_category = score_records.filter(won_count__gte = score_pairs[level][0], won_count__lte = score_pairs[level][1])
        
        # Only do this is someone is logged in, for obvious reasons!
        if current_app_user.is_authenticated:
            if current_user_record in score_category:
                current_user_data["level"] = level
                current_user_data["win_ratio"] = current_user_record.win_ratio
                current_user_data["win_eff"] = current_user_record.win_efficiency
                """
                I have it on the word of some authorities in Django in posts on the SO and DJ  
                that the following is the best way to find the "index" of a particular queryset.
                Apparently, querysets are generator objects, and for some reason prefer to
                be counted rather than being serched for by indexing. 
                Weird, as you can also use slicing on them, which is a form of indexing.
                Hope I clear THAT up soon. Confusing.
                """
                for i in range(len(score_category)):
                    if current_user_record == score_category[i]:
                        current_user_data["place"] = i + 1
                        break
        # print(current_user_data) # Anyway, it works...
        for i in range(3):
            try:
                inner_data = {
                    "player": f"{i + 1} - {score_category[i].user.username}",
                    "won_count": f"{score_category[i].won_count}",
                    "word_count": f"{score_category[i].word_count}",
                    "win_ratio": f"{score_category[i].win_ratio}%",
                    "win_eff": f"{score_category[i].win_efficiency}%"
                }
                
            except IndexError:
                inner_data = {
                    "player": f"{i + 1} - ---",
                    "won_count": "---",
                    "word_count": "---",
                    "win_ratio": "---",
                    "win_eff": "---"
                }
            qlist.append(inner_data.copy())
            
        """
        Seen this before. Do not append the list itself, but a shallow copy of it.
        If the list itself is appended, then when cleared there will be an empty 
        list in the new qlist object. Which is bad, incidentally.
        """
        level_list.append({level: qlist.copy()})
        qlist.clear()
        inner_data.clear()
    
    return (level_list, current_user_data)



def clean_censor():
    """
    A utility function not used by the application.
    Its purpose is to strip the censor file located at 
    https://github.com/whomwah/language-timothy/blob/master/profanity-list.txt
    of words with spaces or words that contain non alpha characters.
    It is to be run from shell, with the text file in the same folder.
    Once the censor file is purged, it should be placed in the wordbank directory.
    """
    with open("en.txt", "r") as file:
        words = []
        words = file.readlines()

    new_list = []
    for word in words:
        if word.replace("\n", "").isalpha():
            new_list.append(word.replace("\n", ""))

    with open("censor.txt", "w") as file:
        for word in new_list:
            file.write(word + " ")

          