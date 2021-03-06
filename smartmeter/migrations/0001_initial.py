# Generated by Django 2.1.4 on 2019-02-11 21:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('create_record_timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('raw_password', models.CharField(max_length=30)),
                ('digest_pass', models.CharField(max_length=30)),
                ('last_send_pwd_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('email', models.CharField(max_length=50)),
            ],
        ),
    ]
