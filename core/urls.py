from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_page, name="home"),
    path("league/<str:league_name>/",views.league_page,name="league_page"),
    path("news/<int:news_id>/",views.news_page,name="news_page"),
]