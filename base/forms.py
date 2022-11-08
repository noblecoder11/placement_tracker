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

def show_domain() : 
    domain_list = Domain.objects.values('name')
    name_list = [] 
    for nm in domain_list : 
        name_list.append(nm['name']) 
    return tuple((nm ,nm) for nm in name_list)

DOMAIN_CHOICES = show_domain()


class PostForm(ModelForm):
    company = forms.ModelChoiceField(queryset= Company.objects.all() )
    intern = forms.BooleanField(initial=False ,required=False)
    ctc = forms.IntegerField()


    class Meta:
        model = Post
        fields = ['title', 'content']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self  , offer_id ,**kwargs) : 
        self.clean()
        self.instance.offer_id = offer_id
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
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class PostFilterForm(forms.Form) : 
    company = forms.ModelChoiceField(queryset=Company.objects.all())
    dream = forms.ChoiceField(choices = (('YES' ,'YES') ,('NO' ,'NO')) )
    domain = forms.ModelChoiceField(queryset= Domain.objects.all() )
    def __init__(self, *args, **kwargs):
        super(PostFilterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
