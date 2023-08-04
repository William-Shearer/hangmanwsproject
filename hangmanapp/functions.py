from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ObjectDoesNotExist
from random import randint
from .models import *

"""
# A test fiunction. Vestigial now. Reference.
def load_words():
    try:
        wordfile = default_storage.open("wordbank/nouns_en.txt")
        words = wordfile.read().decode().split()
        return words
    except FileNotFoundError:
        return False
"""

"""
def convert_to_list(str_word):
    return [c for c in str_word]
"""

"""
def get_word():
    try:
        # Load a file of the wordbank for the game.
        # Note, use Django's own system. It does not like using Python's file loader directly.
        wordfile = default_storage.open("wordbank/nouns_en.txt")
        # This breaks the file content up into a list of strings.
        words = wordfile.read().decode().split()
        # Randomly select a word from the file.
        word = words[randint(0, len(words) - 1)]
        # Return the word as a list of the letters.
        return convert_to_list(word)
    except FileNotFoundError:
        return False
"""


def create_new_word():
    """
    Notes in previous version of get_word apply. The only difference is that
    the word is now returned as a string, and not converted to a Python list.
    """
    try:
        wordfile = default_storage.open("wordbank/nouns_en.txt")
        try:
            words = wordfile.read().decode().split()
            word = words[randint(0, len(words) - 1)]
        except:
            print("Problem reading the file.")
            return False
        else:
            return word
        finally:
            wordfile.close()
    except FileNotFoundError:
        return False


def get_last_user_word(user):
    try:
        word_query = UserWordHistory.objects.filter(user = user, complete = False).order_by("id").last()
        return word_query
    except Exception as error:
        print(f"Query does not exist, creating new word: {error}.")
        if word := create_new_word():
            UserWordHistory.objects.create(
                    user = user,
                    word = word,
                    player_word = "_" * len(word),
                    used_letters = ""
                )
            word_query = UserWordHistory.objects.filter(user = user, complete = False).order_by("id").last()
            return word_query
        else:
            word_query = False
    

if __name__ == "__main__":
    print(create_new_word())
    