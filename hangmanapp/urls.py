from django.urls import path
from . import views

urlpatterns = [
    path("login", views.login_view, name = "login"),
    path("logout", views.logout_view, name = "logout"),
    path("register", views.register_view, name = "register"),
    path("", views.home_page, name = "home"),
    path("game", views.game, name = "game"),
    # API
    path("fetchword", views.fetch_word, name = "fetchword"),
    path("puthistory/<int:word_id>", views.put_history, name = "puthistory"),
    # ERRORS
    path("error", views.general_error, name = "error")
]
