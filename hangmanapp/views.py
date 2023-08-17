from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Sum, Count
# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
# from django.core.exceptions import ObjectDoesNotExist
# from random import randint
from .functions import *
from .models import *
from .forms import *

def login_view(request):
    # return HttpResponse("<h1>Please login</h1>")
    """
    Note: a big gotcha here, noticed quite late in the game.
    The view can NEVER-EVER be called the same thing as a function
    used inside the view function. Makes sense, of course, but it is
    a potential pitfall that is likely to manifest itself
    as familiarity breeds contempt.
    The example here is this:
    I originally called the view plain def login(request):
    This, however, is the same as the actual login function imported
    from django.contrib.auth, and they clash.
    Solution, call the view something else.
    """
    if request.method == "GET":
        context = {"form": LoginForm}
        return render(request, "hangmanapp/login.html", context=context)
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect(reverse("home"))
        else:
            context = {"form": LoginForm, "message": "Incorrect login credentials"}
            return render(request, "hangmanapp/login.html", context = context)
    else:
        return HttpResponse("<h1>Error: Only GET and POST requests here.</h1>")
    
@login_required
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect(reverse("home"))
    else:
        return HttpResponse("<h1>Error: Should not have a POST request.</h1>")


def register_view(request):
    if request.method == "GET":
        context = {"form": RegisterForm}
        return render(request, "hangmanapp/register.html", context = context)
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            confirmation = form.cleaned_data.get("confirmation")
            if password == confirmation:
                try:
                    user = User.objects.create_user(username = username, email = email, password = password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    UserScoreCard.objects.create(user = user)
                except IntegrityError:
                    context = {"form": RegisterForm, "message": "User already exists"}
                    return render(request, "hangmanapp/register.html", context = context)
                else:
                    login(request, user)
                    return redirect(reverse("home"))
            else:
                # return HttpResponse("<h1>Passwords do not match</h1>")
                context = {"form": RegisterForm, "message": "Passwords do not match"}
                return render(request, "hangmanapp/register.html", context = context)
        else:
            return HttpResponse("<h1>Critical Error: Form not valid.</h1>")
    else:
        return HttpResponse("<h1>Critical Error: Not a POST or GET request - this is BAD.</h1>")


def home_page(request):
    if request.method == "GET":
        return render(request, "hangmanapp/home.html")
    else:
        return HttpResponse("<h1>Error: Should not have a POST request.</h1>")

@login_required
def game(request):
    if request.method == "GET":
        return render(request, "hangmanapp/game.html")
    else:
        return HttpResponse("No POST for now.")


def general_error(request):
    return render(request, "hangmanapp/error.html")


def fetch_word(request):
    if request.method == "GET":
        #if word_select := get_last_user_word(request.user):
        if word_select := get_word(request.user):
            """
            Note: get_last_user_word returns an existing word in the DB
            or otherwise creates a new one. Failure of either will return False.
            The data can be sent to JavaScript now as a dict. There, it will be
            treated as a JavaScript object.
            The keys here are used in JavaScript to get the object elements.
            """
            # print(word_select.word)
            word_data = {
                "id": word_select.id,
                "user": request.user.username,
                "word": word_select.word,
                "playerWord": word_select.player_word,
                "hits": word_select.hits,
                "misses": word_select.misses,
                "usedLetters": word_select.used_letters,
                "complete": word_select.complete,
                "won": word_select.won
            }
            # print(word_data["usedLetters"])
            return JsonResponse(word_data)
        else:
            print("ERROR: No way, no how. Word not found. Anywhere.")
            # Actually, don't even send it to JavaScript. word_data is redundant in this case.
            return HttpResponse("ERROR: Bad Things Are Happening.")
            # return redirect(reverse("error"))
            """
            Eventually, it would be a good idea to redirect this to an error html page, 
            where the program may recover. Best bet there would be to perform
            an emergency clean of the DB, and prompt the player to try again with
            an automated fresh start.
            """
    else:
        # No POST or PUT should ever happen, here.
        print("ERROR: A POST/PUT was attempted.")
        return HttpResponse("ERROR: Bad! Very bad! POST/PUT request attempted here.")
        # return redirect(reverse("error"))
    

@csrf_exempt
@login_required
def put_history(request):
    if request.method == "PUT":
        try:
            wObj_data = json.loads(request.body)
            word_DB = UserWordHistory.objects.get(id = wObj_data["id"])
            word_DB.player_word = wObj_data["playerWord"]
            word_DB.hits = wObj_data["hits"]
            word_DB.misses = wObj_data["misses"]
            word_DB.used_letters = wObj_data["usedLetters"]
            word_DB.complete = wObj_data["complete"]
            word_DB.won = wObj_data["won"]
            word_DB.save()
            if word_DB.complete == True:
                if put_score(request.user) == False:
                    print("ERROR: There was an issue saving the score.")
                
            return HttpResponse("DONE")
        except IntegrityError as error:
            print("ERROR: Problem getting the data base record in put_history.")
            return HttpResponse(f"ERROR: In put_history, {error}")
    else:
        print("ERROR: Something other than PUT was attempted in put_history")
        return HttpResponse("ERROR: This is only a PUT function.")
    

