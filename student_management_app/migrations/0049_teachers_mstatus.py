# Generated by Django 3.2.6 on 2021-08-18 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0048_teachers_nid'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='mstatus',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
