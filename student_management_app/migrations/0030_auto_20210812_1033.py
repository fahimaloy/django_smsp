# Generated by Django 3.2.6 on 2021-08-12 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0029_alter_totalmarks_exam_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subjects',
            name='teacher_id',
        ),
        migrations.AlterField(
            model_name='pcc',
            name='batch_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.sectionorbatch'),
        ),
        migrations.AlterField(
            model_name='pcc',
            name='class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.classes'),
        ),
        migrations.AlterField(
            model_name='pcc',
            name='subject_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects'),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='exam_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.examination'),
        ),
        migrations.AlterField(
            model_name='totalmarks',
            name='student_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students'),
        ),
    ]