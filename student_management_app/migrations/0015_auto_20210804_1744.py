# Generated by Django 3.2.5 on 2021-08-04 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0014_alter_students_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='notices',
            name='batch_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sectionorbatch'),
        ),
        migrations.AddField(
            model_name='notices',
            name='class_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.classes'),
        ),
    ]
