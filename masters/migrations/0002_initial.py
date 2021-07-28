# Generated by Django 3.2.5 on 2021-07-28 07:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='main_service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='services.service'),
        ),
        migrations.AddField(
            model_name='master',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='masters.region'),
        ),
        migrations.AddField(
            model_name='master',
            name='services',
            field=models.ManyToManyField(related_name='service_masters', through='services.MasterService', to='services.Service'),
        ),
    ]
