from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login,logout,authenticate
def home(request):
    p = Post.objects.all()
    post_author_list =[]
    for po in p:
        post_author_list.append([po, po.offer_id.student_id])

    posts_len = len(post_author_list) 
    post_author_list = post_author_list[0:min(4,posts_len)]
    
    context ={
        'post' : post_author_list,
    }
    return render(request, 'base/home.html', context) 

def show_all_posts(request) : 
        if request.user.is_authenticated : 
            p = Post.objects.all()
            post_author_list =[]
            for po in p:
                post_author_list.append([po, po.offer_id.student_id])
                # print(po.offer_id)
                # stu = Placement_Detail.objects.get(id = po.offer_id)
                # print(stu)
            print(p)
            print(post_author_list)
                # select student_id from Post natural join Placement_Detail where Post.offer_id=Placement_Detail.id 
            # print("Post objects access query = "  ,p.query)
            
            context ={
                'post' : post_author_list,
            }
        else  : 
            messages.warning(request , 'Login to continue')
            return redirect('home')
        return render(request, 'base/post_list.html' , context)

def create_post(request):
     if request.method == 'POST' : 
        print("here")
        form = PostForm(request.POST)         
        if form.is_valid() : 
            # form.save() 
            userid = request.user.id
            usr =User.objects.get(id =userid)
            print(usr)
            stu =''
            # stu = Student.objects.get(user=usr)
            # stu = Student.objects.get(id= request.user.id)
            company =Company.objects.get(name = form.cleaned_data['company'])
            intern = form.cleaned_data['intern']
            ctc = form.cleaned_data['ctc']
            # offer =Placement_Detail.objects.create(
            #     student_id = stu ,
            #     company_id =company ,
            #     ctc_stipend = ctc ,
            #     intern = intern 
            # )
            print("------ New Offer created -------")
            new_offer = (stu  ,company  ,ctc , intern )
            print(new_offer)
            # form.save(offer_id = offer)
            # form.instance.offer_id = offer
            return HttpResponse("ok")

     else : 

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
            return redirect('login')
        context = { 
            'form' : form
        }
        return render(request, 'base/register.html', context) 
    else : 
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
    stu = Student.objects.get(id = pk)
    offer = Placement_Detail.objects.filter(student_id = stu)
    # print(stu)
    # print(offer)
    # print(offer)
    postlist =[]
    for i in offer : 
        post = Post.objects.filter(offer_id = i.id)
        for p in post  : 
            print(p)
            postlist.append(p)
    context ={}
    print(postlist)
    context['posts'] = postlist 
    context['student'] = stu
    return render(req , 'base/profile.html' ,context)


def about(req):
    return render(req , 'base/about.html')

def post_detail(req ,pk):
    author_post = Post.objects.get(id =pk)
    # print(author_post)
    context  = {
        'post' : author_post
    }
    return render(req, 'base/post_detail.html' , context )