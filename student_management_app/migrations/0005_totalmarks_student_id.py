# Generated by Django 3.2.5 on 2021-07-16 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0004_totalmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalmarks',
            name='student_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students'),
        ),
    ]
