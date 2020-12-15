# Generated by Django 3.1.3 on 2021-03-23 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='longitude',
        ),
        migrations.AddField(
            model_name='subject',
            name='latitude',
            field=models.FloatField(default=10.3344277),
        ),
        migrations.AddField(
            model_name='subject',
            name='longitude',
            field=models.FloatField(default=123.8791918),
        ),
    ]