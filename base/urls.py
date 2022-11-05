from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', views.home, name='home'),
    path('create/' , views.create_post, name='new_post'),
    path('register/' , views.user_register, name ='register'),
    path('login/' , views.user_login, name ='login'),
    path('logout/' , views.user_logout, name ='logout'),
    path('allposts/' , views.show_all_posts, name ='all_posts'),
    path('profile/<int:pk>' , views.my_profile, name ='profile'),
    path('post/<int:pk>' , views.post_detail, name ='post-detail'),
    path('about/', views.about, name='about'),
]