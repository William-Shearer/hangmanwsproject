from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.db import IntegrityError
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
    

def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect(reverse("login"))


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
            return HttpResponse("<h1>Critical Error: Form not valid</h1>")
    else:
        return HttpResponse("<h1>Critical Error: Not a POST or GET request - this is BAD</h1>")


def home_page(request):
    if request.method == "GET":
        if not request.user.is_authenticated:
            return redirect(reverse("login"))
        else:
            return render(request, "hangmanapp/home.html")
    else:
        return HttpResponse("<h1>Error: Should not have a POST request (yet)</h1>")


def game(request):
    if request.method == "GET":
        return render(request, "hangmanapp/game.html")
    else:
        return HttpResponse("No POST for now")


def fetch_word(request):
    if request.method == "GET":
        if word := get_word():
            data_word = {
                "userId": request.user.id,
                "userName": request.user.username,
                "word": word}
            return JsonResponse(data_word)
        else:
            data_word = {"word": ["f", "o", "o"]}
            print("Error: Word not found")
            return JsonResponse(data_word)
    else:
        return HttpResponse("Error: POST request attempted")
    
