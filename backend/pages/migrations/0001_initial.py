# Generated by Django 3.1.1 on 2020-12-15 03:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
            ],
            options={
                'db_table': 'Comments',
            },
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardOwnerName', models.TextField(default=None, max_length=100)),
                ('cardNumber', models.IntegerField(blank=True, default=None, null=True)),
                ('expire_month', models.IntegerField(blank=True, default=None, null=True)),
                ('expire_year', models.IntegerField(blank=True, default=None, null=True)),
                ('cvc', models.IntegerField(blank=True, default=None, null=True)),
            ],
            options={
                'db_table': 'Details',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(blank=True, max_length=100, null=True)),
                ('middleName', models.CharField(blank=True, max_length=100, null=True)),
                ('lastName', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contactNo', models.IntegerField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
            ],
            options={
                'db_table': 'Ratings',
            },
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.CharField(default='', max_length=100)),
            ],
            options={
                'db_table': 'Receipt',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.CharField(default='00:00-00:00', max_length=10, null=True)),
                ('custom_time_start', models.CharField(default='00:00', max_length=10, null=True)),
                ('custom_time_end', models.CharField(default='00:00', max_length=10, null=True)),
                ('ratePrHour', models.DecimalField(decimal_places=2, default='0', max_digits=5, null=True)),
                ('payment_method', models.CharField(default='', max_length=10, null=True)),
                ('status', models.BooleanField(default=False)),
                ('latitude', models.FloatField(default=10.3344277)),
                ('longitude', models.FloatField(default=123.8791918)),
            ],
            options={
                'db_table': 'Schedule',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjectName', models.CharField(default='', max_length=100)),
                ('ratePerHour', models.DecimalField(decimal_places=2, default='0', max_digits=5)),
                ('session_date', models.DateField(default=None)),
                ('session_time_end', models.CharField(default='00:00', max_length=10)),
                ('session_time_start', models.CharField(default='00:00', max_length=10)),
                ('category', models.CharField(default='', max_length=30)),
            ],
            options={
                'db_table': 'Subject',
            },
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.profile')),
                ('position', models.CharField(default=None, max_length=50)),
            ],
            options={
                'db_table': 'Admin',
            },
            bases=('pages.profile',),
        ),
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.profile')),
                ('bio', models.CharField(default=None, max_length=100)),
            ],
            options={
                'db_table': 'Mentee',
            },
            bases=('pages.profile',),
        ),
        migrations.CreateModel(
            name='Mentor',
            fields=[
                ('profile_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pages.profile')),
                ('achvemnts', models.BooleanField()),
                ('proofs', models.BooleanField()),
            ],
            options={
                'db_table': 'Mentor',
            },
            bases=('pages.profile',),
        ),
        migrations.CreateModel(
            name='TutorialPayment',
            fields=[
                ('id', models.AutoField(default=None, primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('scheduleID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.schedule')),
            ],
            options={
                'db_table': 'TutorialPayment',
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.subject'),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.details')),
                ('receiptID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.receipt')),
                ('userID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.profile')),
            ],
            options={
                'db_table': 'Account',
            },
        ),
        migrations.AddField(
            model_name='subject',
            name='mentorID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentor'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='menteeID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentee'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comments', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.comments')),
                ('ratings', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.ratings')),
                ('menteeID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentee')),
                ('mentorID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentor')),
            ],
            options={
                'db_table': 'Review',
            },
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(default=' ', max_length=500, null=True)),
                ('notesTitle', models.CharField(default=' ', max_length=500, null=True)),
                ('subjectID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.subject')),
                ('menteeID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentee')),
                ('mentorID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentor')),
            ],
            options={
                'db_table': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('menteeID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='pages.mentee')),
            ],
            options={
                'db_table': 'Messages',
            },
        ),
    ]
