# Generated by Django 3.2.11 on 2022-02-05 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0065_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feesreport',
            name='extra_amount',
            field=models.IntegerField(default=0),
        ),
    ]