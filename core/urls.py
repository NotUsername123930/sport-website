from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home_page, name="home"),
    path("league/<str:league_name>/", views.league_page, name="league_page"),
    path("news/<int:news_id>/", views.news_page, name="news_page"),
    path("accounts/register/", views.register, name="register"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
        ),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="home"),
        name="logout",
    ),
    path("news/<int:news_id>/comment/", views.post_comment, name="post_comment"),
    path("news/", views.news_archive, name="news_archive"),
    path("updates/", views.updates_archive, name="updates_archive"),
]