# Generated by Django 3.1.1 on 2020-12-08 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0008_auto_20201208_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='session_time',
            field=models.CharField(default=None, max_length=20),
        ),
    ]