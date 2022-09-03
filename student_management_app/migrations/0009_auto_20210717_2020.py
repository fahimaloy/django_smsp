# Generated by Django 3.2.5 on 2021-07-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0008_auto_20210717_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='totalmarks',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='totalmarks',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
