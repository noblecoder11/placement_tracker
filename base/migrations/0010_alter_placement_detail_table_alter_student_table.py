# Generated by Django 4.1.3 on 2022-11-07 02:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_alter_placement_detail_intern'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='placement_detail',
            table='Placement_Detail',
        ),
        migrations.AlterModelTable(
            name='student',
            table='Student',
        ),
    ]
