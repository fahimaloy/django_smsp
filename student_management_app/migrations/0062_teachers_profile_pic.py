# Generated by Django 3.2.6 on 2021-12-27 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0061_auto_20211226_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='profile_pic',
            field=models.FileField(null=True, upload_to=''),
        ),
    ]
