# Generated by Django 3.2.2 on 2021-05-13 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0014_remove_gallery_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='mybooking',
            name='address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
