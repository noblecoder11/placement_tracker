from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login,logout,authenticate
def home(request):
    p = Post.objects.all()
    print("Post objects access query = "  ,p.query)
    context ={
        'post' : p
    }
    return render(request, 'base/home.html', context) 

def create_post(request):
    post_form = PostForm()
    context = { 
        'post_form' : post_form
    }
    return render(request, 'base/postcreate.html', context) 

def user_login(request) : 
    print("here")
    if request.method =='POST' : 
        form = LoginForm(request.POST)
        if form.is_valid() : 
            form.save()
            return redirect('home')
    form = LoginForm()
    context = { 
        'form' : form
    }
    return render(request, 'base/login.html', context) 
