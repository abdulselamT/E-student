# Generated by Django 3.2.7 on 2021-09-12 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_teacher_propic'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='logo',
            field=models.ImageField(default='profile1.jpg', null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='student',
            name='propic',
            field=models.ImageField(default='profile1.jpg', null=True, upload_to=''),
        ),
    ]