# Generated by Django 3.1.1 on 2020-11-09 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20201109_1513'),
    ]

    operations = [
        migrations.DeleteModel(
            name='tenant',
        ),
    ]