# Generated by Django 3.1.1 on 2020-12-07 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='session_date',
        ),
    ]
