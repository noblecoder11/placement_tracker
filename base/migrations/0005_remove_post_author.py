# Generated by Django 4.1.3 on 2022-11-03 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_student_roll'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
    ]
