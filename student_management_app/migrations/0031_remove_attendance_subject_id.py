# Generated by Django 3.2.6 on 2021-08-12 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0030_auto_20210812_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendance',
            name='subject_id',
        ),
    ]