# Generated by Django 5.0.6 on 2024-12-25 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_tutorlinc', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='teaching_experience',
            field=models.IntegerField(default=0),
        ),
    ]
