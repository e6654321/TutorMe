# Generated by Django 3.1.1 on 2020-12-14 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0019_auto_20201215_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='custom_time_end',
            field=models.CharField(default='00:00', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='custom_time_start',
            field=models.CharField(default='00:00', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='payment_method',
            field=models.CharField(default='', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='ratePrHour',
            field=models.DecimalField(decimal_places=2, default='0', max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.CharField(default='00:00-00:00', max_length=10, null=True),
        ),
    ]
