# Generated by Django 4.1.3 on 2022-11-07 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_alter_placement_detail_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='company',
            table='Company',
        ),
        migrations.AlterModelTable(
            name='department',
            table='Department',
        ),
        migrations.AlterModelTable(
            name='domain',
            table='Domain',
        ),
    ]
