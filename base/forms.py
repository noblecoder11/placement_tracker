from django.forms import ModelForm 
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class LoginForm(ModelForm) : 
    # password = models.CharField(max_length=100)
    # confirm_password = models.CharField(max_length=100)
    class Meta:
        model = Student
        fields = ['name', 'year_of_passing', 'dept_id']
        success_url = reverse_lazy('/')
        

   
