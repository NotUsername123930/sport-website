from django.contrib import admin
from django.urls import path, include
from core import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path("league/<str:league_name>/",views.league_page,name="league_page"),
]
