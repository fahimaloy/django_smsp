# Generated by Django 3.2.5 on 2021-07-17 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0009_auto_20210717_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalmarks',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='totalmarks',
            name='updated_at',
            field=models.DateTimeField(),
        ),
    ]
