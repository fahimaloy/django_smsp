# Generated by Django 3.2.6 on 2021-08-19 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0049_teachers_mstatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='batch_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sectionorbatch'),
        ),
    ]
