# Generated by Django 3.2.6 on 2021-08-06 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0022_auto_20210805_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='examination',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]