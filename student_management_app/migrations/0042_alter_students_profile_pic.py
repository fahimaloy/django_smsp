# Generated by Django 3.2.6 on 2021-08-14 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0041_alter_students_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.FileField(upload_to=''),
        ),
    ]
