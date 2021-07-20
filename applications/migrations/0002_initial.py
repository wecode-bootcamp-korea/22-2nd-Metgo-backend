# Generated by Django 3.2.5 on 2021-07-21 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
        ('users', '0001_initial'),
        ('applications', '0001_initial'),
        ('masters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationmaster',
            name='master',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masters.master'),
        ),
        migrations.AddField(
            model_name='application',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='masters.region'),
        ),
        migrations.AddField(
            model_name='application',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
