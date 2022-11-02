from django.forms import ModelForm 
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .helpers import current_year ,years
DEPT_CHOICES = [
    ('CS', 'Computer Science'),
    ('IT', 'Information Technology'),
    ('ENTC', 'Electronics and Telecommunication'),
]

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class LoginForm(ModelForm) : 
    password = forms.CharField(max_length=100)
    confirm_password = forms.CharField(max_length=100 ,
        widget = forms.PasswordInput() ,
    )
    class Meta:
        model = Student
        fields = ['name', 'year_of_passing', 'dept_id']
        success_url = reverse_lazy('/')

    def clean(self):
        super(LoginForm ,self).clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Two passwords do not match'])
            # raise forms.ValidationError(
            #     "password and confirm_password does not match"
            # )

        return self.cleaned_data
        
    #  def clean_email(self):
    #         email = self.cleaned_data.get('email')
    #         username = self.cleaned_data.get('username')

    #         if email and User.objects.filter(email=email).exclude(username=username).count():
    #             raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
    #         return email
