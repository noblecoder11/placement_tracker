# Generated by Django 4.1.3 on 2022-11-09 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_placement_detail_intern'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='domain_id',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='base.domain'),
            preserve_default=False,
        ),
    ]
