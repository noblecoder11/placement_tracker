from django.contrib import admin
from .models import * 
from django.contrib.auth.models import User    
from django.contrib.auth.admin import UserAdmin

# @admin.register(User)
UserAdmin.list_display = ['username' , 'id' , 'is_active']
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin) : 
    list_display = ['id' ,'name' , 'dept_id' , 'year_of_passing' , 'user' ]
    
@admin.register(Placement_Detail)
class StudentAdmin(admin.ModelAdmin) : 
    list_display = ['id' ,'student_id' , 'company_id' , 'intern']

admin.site.register(Department)
admin.site.register(Domain)
admin.site.register(Company)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin) : 
    list_display = ['id' ,'title' ,'offer_id']