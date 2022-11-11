from django.shortcuts import render ,redirect 
from django.urls import reverse
from django.http import HttpResponse
from django.db import connection
from .models import *
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login,logout,authenticate
from django.views.generic import DeleteView
from django.contrib.auth.decorators import login_required 
import random
from datetime import datetime

def home(request):
    
    postlist =[]
    for po in Post.objects.raw("SELECT * FROM posts"):
        postlist.append(po)
    post_author_list =[]
    
    for i in range (0,min(len(postlist) ,4)) : 
        ele =(random.choice(postlist))
        post_author_list.append(ele)
        postlist.remove(ele)
    context ={
        'post' : post_author_list ,
    
    }
    return render(request, 'base/home.html', context) 

def show_all_posts(request ) : 
        if request.user.is_authenticated : 

            comapnies =[]
            for c in Company.objects.raw("SELECT * FROM Company") : 
                comapnies.append(c)
         
            #FILTER FORM LOGIC
            
            company = request.GET.get('company') 
            dream = request.GET.get('dream') or ''
            domain = request.GET.get('domain') or '' 
            print("company = " ,company)
            post = []        
            if company != 'All'  : 
                print("inside company ")
                for p in Post.objects.raw("SELECT * FROM posts WHERE offer_id_id in (SELECT id from Placement_Detail  WHERE company_id_id in (SELECT id from Company WHERE name =%s))" ,[company]) :    
                    post.append(p)
            elif dream != 'All' and domain != 'All':
                print("inside dream and domain")
                for p in Post.objects.raw("SELECT * FROM posts WHERE offer_id_id in (SELECT id from Placement_Detail  WHERE company_id_id in (SELECT id from Company WHERE dream =%s and domain_id_id=%s))" ,[company ,domain]) :    
                    post.append(p)
                
                    # cursor.execute("SELECT * FROM Company WHERE dream=%s" ,)
            elif dream != 'All' : 
                for p in Post.objects.raw("SELECT * FROM posts WHERE offer_id_id in (SELECT id from Placement_Detail  WHERE company_id_id in (SELECT id from Company WHERE dream =%s ))" ,[dream]) :   
                    post.append(p)
                #  print(p.offer_id_id)
            else : 
                for p in Post.objects.raw("SELECT * FROM posts") : 
                    post.append(p)
            context ={
                'post' : post,
            
                'companies' : comapnies
            }
        else  : 
            messages.warning(request , 'Login to continue')
            return redirect('home')
        return render(request, 'base/post_list.html' , context)


def user_login(req):
    if req.method == 'POST' : 
        form = LoginForm(req.POST) 
        if form.is_valid() : 
            nm = form.cleaned_data['name']
            pw = form.cleaned_data['password']
            print("Name  = " + nm ,' Password = ' ,pw)
            stu = authenticate(req , username = nm ,password = pw)
            if stu is not None : 
                login(req , stu)
                return redirect('home')       
        messages.warning(req , 'Invalid credentials')
        context = {
                    'form' : form
        }
        return render(req , 'base/login.html' ,context)
    else : 
        form = LoginForm()
        return render(req , 'base/login.html' , {'form' : form})

@login_required(login_url='login')   
def user_logout(req) : 
    logout(req)
    return redirect('home')

@login_required(login_url='login')   
def my_profile(req , pk) : 
    
    for s in Student.objects.raw("SELECT * FROM student WHERE id = %s" ,[pk]) : 
        stu = s; 
    postlist =[]
    for i in Placement_Detail.objects.raw("SELECT *  FROM Placement_Detail WHERE student_id_id = %s",[pk]) : 
        for p in Post.objects.raw("SELECT * FROM posts where offer_id_id = %s" ,[i.id])  : 
            postlist.append(p)
    context ={}
    context['posts'] = postlist 
    context['student'] = stu
    return render(req , 'base/profile.html' ,context)


def about(req):
    return render(req , 'base/about.html')

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


@login_required(login_url='login')
def create_post(request):
     if request.method == 'POST' : 
        form = PostForm(request.POST)         
        if form.is_valid() : 
            usr = request.user
            stu =''
            for s in  Student.objects.raw("SELECT * FROM student WHERE user_id = %s" ,[usr.id]) :
                stu =  s.id
            name = form.cleaned_data['company']
            print(name)
            intern = form.cleaned_data['intern']
            ctc = form.cleaned_data['ctc']
            for c in Company.objects.raw("SELECT * FROM Company WHERE name = %s" ,[name]):
                company = c.id
            with connection.cursor() as cursor  : 
                cursor.execute("INSERT INTO Placement_Detail(ctc_stipend ,intern,company_id_id,student_id_id) VALUES (%s,%s,%s,%s)"  ,
                [ctc,intern,company,stu])
            for res in Placement_Detail.objects.raw("SELECT * FROM Placement_Detail order by id desc LIMIT 1") : 
                offer = (res)       
            form.save(offer_id = offer)
            new_offer = (stu  ,company  ,ctc , intern ,offer)
            print("------ NEW OFFER CREATED ------")
            print(new_offer)
            return redirect(reverse('profile' ,kwargs={"pk" : stu}))

     else :
        post_form = PostForm()
        context = { 
            'post_form' : post_form
        }
        return render(request, 'base/postcreate.html', context) 


@login_required(login_url='login')
def delete_post(req ,pk) : 
    with connection.cursor() as cursor : 
        cursor.execute("SELECT id FROM student WHERE user_id = %s " ,[req.user.id])
        stuid = cursor.fetchone()[0]
    if req.method == 'POST' : 
        with connection.cursor() as cursor : 
            cursor.execute("SELECT offer_id_id from posts WHERE id =%s" ,[pk])
            pid = cursor.fetchone()[0]
            cursor.execute("DELETE FROM posts WHERE id =%s" ,[pk])
            cursor.execute("DELETE FROM Placement_Detail WHERE id =%s" ,[pid])
            return redirect(reverse('profile' , kwargs={'pk' : stuid}))
    elif req.method == 'GET' : 
        return render(req ,'base/post_confirm_delete.html' ,{'id' :stuid})

@login_required(login_url='login')
def update_post(req , pk) : 
    with connection.cursor() as cursor : 
        cursor.execute("SELECT id FROM student WHERE user_id = %s " ,[req.user.id])
        stuid = cursor.fetchone()[0]
    if req.method == 'POST' : 
        form = PostForm(req.POST) 
        if form.is_valid() : 
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            ctc= form.cleaned_data['ctc']
            intern = form.cleaned_data['intern']
            company = form.cleaned_data['company']

            print("updated intern = " , intern)

            for p in  Placement_Detail.objects.raw("SELECT * FROM Placement_Detail WHERE id =  (SELECT offer_id_id from posts WHERE id = %s)" ,[pk]) : 
             pobj = p  
            print("POBJ id = " , pobj.id)
            print("initial intern =" ,pobj.intern)
            for d in Company.objects.raw("SELECT id FROM Company WHERE name = %s" ,[company]) : 
                company_obj = d
            
            same = True
            if pobj.company_id.name != company or pobj.ctc_stipend != ctc or pobj.intern != intern :
                same = False 
            print("same = " ,same)
            if same == False : 
                with connection.cursor() as cursor : 
                    cursor.execute("UPDATE Placement_Detail SET company_id_id =%s , ctc_stipend =%s ,intern =%s WHERE id =%s" ,[company_obj.id ,ctc ,intern,pobj.id])
                    
            
            updated_time = datetime.now()
            with connection.cursor() as cursor : 
                cursor.execute("UPDATE posts SET title=%s ,content=%s  ,updated_at=%s WHERE offer_id_id =%s" ,[title,content,updated_time ,pobj.id])
        messages.success(req ,"Post Updated successfully")
        return redirect(reverse('profile' ,kwargs={'pk' : stuid }))
    elif req.method == 'GET' :
        for p in Post.objects.raw("SELECT * FROM posts WHERE id = %s" ,[pk]):
            post_object = p 
        for p in Placement_Detail.objects.raw("SELECT * FROM Placement_Detail WHERE id =(SELECT offer_id_id FROM posts WHERE id =%s)" ,[pk]) : 
            placement_object = p
        data = {
        "title" : f"{post_object.title}",
        "content" : f"{post_object.content}",
        "ctc":f"{placement_object.ctc_stipend}",
        "intern":f"{placement_object.intern}",
        "company":f"{placement_object.company_id}",
         }
        print(data)
        form = PostForm(initial =data)
        return render(req , 'base/post_update.html' ,{'post_form' : form})

def post_detail(req ,pk):
    for p in  Post.objects.raw("SELECT * FROM posts WHERE id = %s" ,[pk]) : 
        author_post = p 
    context  = {
        'post' : author_post
    }
    return render(req, 'base/post_detail.html' , context )