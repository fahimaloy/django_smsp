# Generated by Django 3.2.6 on 2021-08-12 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0032_studentresult_teacher_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentresult',
            name='teacher_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.teachers'),
        ),
    ]
