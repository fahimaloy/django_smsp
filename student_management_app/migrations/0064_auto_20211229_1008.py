# Generated by Django 3.2.6 on 2021-12-29 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0063_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='link',
            field=models.CharField(default='', max_length=555),
        ),
        migrations.AlterField(
            model_name='notifications',
            name='title',
            field=models.CharField(max_length=555),
        ),
    ]
