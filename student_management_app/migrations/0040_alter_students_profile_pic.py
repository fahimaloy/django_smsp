# Generated by Django 3.2.6 on 2021-08-14 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0039_auto_20210814_2117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.FileField(upload_to='images/'),
        ),
    ]
