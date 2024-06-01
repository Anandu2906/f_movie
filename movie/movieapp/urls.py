from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home,name="home"),
    path('index', views.index,name="index"),
    path('user_signup', views.user_signup, name="user"),
    path('user_signupp', views.user_signupp, name="home"),
    path('user_login', views.user_login, name="login"),
    path('user_loginn', views.user_loginn, name="loginn"),
    path('ulogout', views.ulogout, name="logout"),
    path('uhome', views.uhome,name="logout"),
    path('add_video', views.add_video, name="add_video"),
    path('view_video', views.view_video, name="view_video"),
    path('udel_video', views.udel_video, name="udel_video"),
    path('uedit_video', views.uedit_video, name="uedit_video"),
    path('update_video', views.update_video, name="update_video"),
    path('uprofile', views.uprofile, name="uprofile"),
    path('uedit_profile', views.uedit_profile, name="uedit_profile"),
    path('uedit_profile', views.uedit_profile, name="uedit_profile"),
    path('movies', views.movies, name="movies"),
    path('post_review', views.post_review, name="post_review"),
    path('submit_review', views.submit_review, name="submit_review"),
    path('search', views.search_movies, name="search"),
    path('show', views.showmovies, name="show"),
]