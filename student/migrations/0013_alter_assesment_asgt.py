# Generated by Django 3.2.7 on 2021-09-12 08:56

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_auto_20210912_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assesment',
            name='asgt',
            field=jsonfield.fields.JSONField(default={}, null=True),
        ),
    ]
