# Generated by Django 4.1.3 on 2022-11-07 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_company_table_alter_department_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placement_detail',
            name='intern',
            field=models.BooleanField(),
        ),
    ]