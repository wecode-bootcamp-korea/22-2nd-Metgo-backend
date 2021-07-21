# Generated by Django 3.2.5 on 2021-07-20 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.IntegerField()),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('birth', models.DateField()),
                ('profile_image', models.URLField()),
                ('career', models.IntegerField()),
            ],
            options={
                'db_table': 'masters',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'regions',
            },
        ),
    ]
