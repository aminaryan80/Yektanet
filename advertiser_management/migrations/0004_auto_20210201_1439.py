# Generated by Django 3.1.5 on 2021-02-01 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_baseadactions_click_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ad',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='ad',
            name='views',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='clicks',
        ),
        migrations.RemoveField(
            model_name='advertiser',
            name='views',
        ),
    ]