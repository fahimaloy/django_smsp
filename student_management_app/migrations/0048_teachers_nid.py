# Generated by Django 3.2.6 on 2021-08-17 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0047_alter_classandpayment_class_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachers',
            name='nid',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
