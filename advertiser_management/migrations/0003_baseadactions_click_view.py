# Generated by Django 3.1.5 on 2021-02-01 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0002_remove_ad_link'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAdActions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('ip', models.CharField(max_length=16)),
                ('ad_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertiser_management.ad')),
            ],
        ),
        migrations.CreateModel(
            name='Click',
            fields=[
                ('baseadactions_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advertiser_management.baseadactions')),
            ],
            bases=('advertiser_management.baseadactions',),
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('baseadactions_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='advertiser_management.baseadactions')),
            ],
            bases=('advertiser_management.baseadactions',),
        ),
    ]