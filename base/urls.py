from django.shortcuts import render
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', views.home, name='home'),
    path('create/' , views.create_post, name='new_post'),
    path('login/' , views.user_login, name ='login')
]