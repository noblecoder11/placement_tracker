# Generated by Django 4.1.3 on 2022-11-05 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0007_alter_post_offer_id_alter_student_year_of_passing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stud', to=settings.AUTH_USER_MODEL),
        ),
    ]
