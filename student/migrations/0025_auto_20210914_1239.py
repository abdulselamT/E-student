# Generated by Django 3.2.7 on 2021-09-14 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0024_student_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='status',
        ),
        migrations.AddField(
            model_name='assesment',
            name='status',
            field=models.CharField(blank=True, choices=[('red', 'red'), ('green', 'green'), ('yellow', 'yellow')], max_length=200, null=True),
        ),
    ]
