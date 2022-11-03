from django.forms import ModelForm 
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .helpers import current_year ,years 
from django.contrib import messages
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
    print(name_list)
    d = tuple((nm ,nm) for nm in name_list)
    print(d)
    return tuple((nm ,nm) for nm in name_list)

COMPANY_CHOICES = show_companies()
class PostForm(ModelForm):
    company = forms.ChoiceField(choices = COMPANY_CHOICES )
    intern = forms.BooleanField()
    ctc = forms.IntegerField()
    class Meta:
        model = Post
        fields = ['title', 'content']


class RegisterForm(ModelForm) : 
    password = forms.CharField(max_length=100)
    confirm_password = forms.CharField(max_length=100 ,
        widget = forms.PasswordInput() ,
        error_messages= {'invalid':'Two passwords do no match'}
    )
    class Meta:
        model = Student
        fields = ['name', 'year_of_passing', 'dept_id']
        success_url = reverse_lazy('/')

    def clean(self):
        super(RegisterForm ,self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            # self._errors['password'] = self.error_class(['Two passwords do not match'])
            # messages.warning(self.request , 'Two passwords do not match')
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        return self.cleaned_data
        

class LoginForm(ModelForm) :
    password = forms.CharField(
        widget=forms.PasswordInput()
    ) 
    class Meta  : 
        model = Student
        fields =['name']
    #  def clean_email(self):
    #         email = self.cleaned_data.get('email')
    #         username = self.cleaned_data.get('username')

    #         if email and User.objects.filter(email=email).exclude(username=username).count():
    #             raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
    #         return email
