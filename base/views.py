from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login,logout,authenticate
def home(request):
    p = Post.objects.all()
    posts_len = len(p) 
    p = p[0:min(4,posts_len)]
    # print("Post objects access query = "  ,p.query)
    context ={
        'post' : p
    }
    return render(request, 'base/home.html', context) 

def show_all_posts(request) : 
    if request.user.is_authenticated : 
        p = Post.objects.all()
        # print("Post objects access query = "  ,p.query)
        context ={
            'post' : p
        }
    else  : 
        messages.warning(request , 'Login to continue')
        return redirect('home')
    return render(request, 'base/post_list.html' , context)

def create_post(request):
    post_form = PostForm()
    context = { 
        'post_form' : post_form
    }
    return render(request, 'base/postcreate.html', context) 

def user_register(request) : 
    if request.method =='POST' : 
        form = RegisterForm(request.POST)
        if form.is_valid() : 
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            yop = form.cleaned_data['year_of_passing']
            dept_id = form.cleaned_data['dept_id']

            user =User.objects.create(username = name)
            user.set_password(password)
            user.save()
            stu = Student.objects.create(
                name = name , 
                year_of_passing = yop  ,
                dept_id = dept_id ,
                user = user
            )
            print(f"Student created with name{name} ")
            # form.save()
            return redirect('login')
    form = RegisterForm()
    context = { 
        'form' : form
    }
    return render(request, 'base/register.html', context) 

def user_login(req):
    if req.method == 'POST' : 
        form = LoginForm(req.POST) 
        if form.is_valid() : 
            nm = form.cleaned_data['name']
            pw = form.cleaned_data['password']
            print(nm ,' ' ,pw)
            stu = authenticate(req , username = nm ,password = pw)
            print(stu)
            if stu is not None : 
                login(req , stu)
                return redirect('home')
    form  = LoginForm()
    context = {
        'form' : form
    }
    return render(req , 'base/login.html' ,context)

def user_logout(req) : 
    logout(req)
    return redirect('home')
def my_profile(req , pk) : 
    offer = Placement_Detail.objects.filter(student_id = pk)
    # print(offer)
    postlist =[]
    for i in offer : 
        post = Post.objects.filter(offer_id = i.id)
        for p in post  : 
            print(p)
            postlist.append(p)
    context ={}
    context['posts'] = postlist 
    # context['student'] = stu 
    return render(req , 'base/profile.html' ,context)


def about(req):
    return render(req , 'base/about.html')