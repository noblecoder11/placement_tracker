from django.forms import ModelForm 
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .helpers import current_year ,years 
from django.contrib import messages
# from django.core.exceptions import ValidationError
DEPT_CHOICES = [
    ('CS', 'Computer Science'),
    ('IT', 'Information Technology'),
    ('ENTC', 'Electronics and Telecommunication'),
]

def show_companies() : 
    company_list = Company.objects.values('name')
    name_list = [] 
    for nm in company_list : 
        name_list.append(nm['name']) 
    return tuple((nm ,nm) for nm in name_list)

COMPANY_CHOICES = show_companies()
class PostForm(ModelForm):
    company = forms.ChoiceField(choices = COMPANY_CHOICES )
    intern = forms.BooleanField()
    ctc = forms.IntegerField()
    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self ,**kwargs) : 
        self.clean()
        oid = kwargs['offer_id']
        print(oid)
        self.cleaned_data['offer_id'] = oid
        return super(PostForm ,self).save(**kwargs)



class RegisterForm(ModelForm) : 
    password = forms.CharField( min_length=4,max_length=100 ,
     widget = forms.PasswordInput() ,
    )
    confirm_password = forms.CharField(min_length =4 , max_length=100 ,
        widget = forms.PasswordInput() ,
    )
    class Meta:
        model = Student
        fields = ['name', 'year_of_passing', 'dept_id']
    
    def clean(self):
        super(RegisterForm ,self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password : 
            print("Passwords do not match")
            raise forms.ValidationError(
                "passwords do not match"
            )
        return self.cleaned_data

    def clean_name(self) : 
        username = self.cleaned_data['name']
        try : 
            user = User.objects.get(username = username)
        except User.DoesNotExist : 
            return username
        print("Username already in use")
        raise forms.ValidationError(
            'Username already in use' 
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

   
class LoginForm(ModelForm) :
    password = forms.CharField(
        widget=forms.PasswordInput()
    ) 
    class Meta  : 
        model = Student
        fields =['name']

    def clean_name(self) : 
        username = self.cleaned_data['name']
        try : 
            user = User.objects.get(username = username)
        except User.DoesNotExist : 
            raise forms.ValidationError(
                'User does not exist . Please login' 
            )
        return username
