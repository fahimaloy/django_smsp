# Generated by Django 3.2.6 on 2021-08-22 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0054_auto_20210822_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineclass',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.customuser'),
        ),
    ]
