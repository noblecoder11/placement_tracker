from django.db import models
from django.contrib.auth.models import User
from .helpers import current_year , years
class Department(models.Model) : 
    name = models.CharField(max_length=100)
    def __str__(self) :
        return self.name
    class Meta : 
        db_table = 'Department'

class Student(models.Model) :
    name = models.CharField(max_length=100)
    year_of_passing =models.IntegerField(('year_of_passing'), choices=years, default=current_year)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    user = models.ForeignKey(User ,on_delete = models.CASCADE ,related_name ='stud')
    def __str__(self) : 
        return self.name

    class Meta : 
        db_table = 'student'

class Domain(models.Model) : 
    name = models.CharField(max_length=100)
    def __str__(self) : 
        return self.name
    class Meta : 
        db_table = 'Domain'

class Company(models.Model) :
    name = models.CharField(max_length=100)
    dream = models.BooleanField(default=False)
    domain_id = models.ForeignKey(Domain, on_delete=models.CASCADE)
    class Meta :
        db_table = 'Company'
        verbose_name = ("Company")
        verbose_name_plural = ("Companies")
    def __str__(self) : 
        return self.name
    
class Placement_Detail(models.Model) :
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    ctc_stipend = models.IntegerField()
    intern = models.BooleanField(default=False )
    class Meta : 
        db_table ='Placement_Detail'

    

class Post(models.Model) :
    title = models.CharField(max_length=100)
    content = models.TextField()
    offer_id = models.ForeignKey(Placement_Detail ,on_delete = models.CASCADE ,related_name = 'offer')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta : 
        db_table = 'posts'

    