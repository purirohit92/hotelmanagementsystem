# Generated by Django 3.2.2 on 2021-05-18 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0017_auto_20210516_1051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mybooking',
            name='arrival_date',
        ),
        migrations.RemoveField(
            model_name='mybooking',
            name='departure_date',
        ),
    ]
