# Generated by Django 3.2.5 on 2021-07-16 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0005_totalmarks_student_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalmarks',
            name='obtained_marks',
            field=models.IntegerField(default=0),
        ),
    ]
