from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register_view, name = "register"),
    path("changepwd", views.change_pword, name = "changepwd"),
    path("", views.home_page, name = "home"),
    path("game", views.game, name = "game"),
    path("history", views.history_view, name = "history"),
    # API
    path("fetchword", views.fetch_word, name = "fetchword"),
    path("puthistory", views.put_history, name = "puthistory"),
    # path("putuserscore", views.put_score, name = "putuserscore"), # suppressed.
    # ERRORS
    path("error", views.general_error, name = "error")
]
