from django.urls import path 
from . import views


urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("news/", views.news, name="news"),
    path("breachbites/", views.breachbites, name="breachbites"),
    path("", views.home, name="home"),
    path("logout", views.logout_view, name="logout"),
    path("resources/", views.resources, name="resources"),

]