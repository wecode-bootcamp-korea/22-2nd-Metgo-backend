# Generated by Django 3.2.5 on 2021-07-25 06:07

from django.db import migrations, models
import django.db.models.deletion


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
                ('kakao_id', models.IntegerField(null=True, unique=True)),
                ('certification', models.BooleanField(null=True)),
                ('business', models.BooleanField(null=True)),
                ('introduction', models.CharField(max_length=100, null=True)),
                ('description', models.CharField(max_length=300, null=True)),
                ('name', models.CharField(max_length=45, null=True)),
                ('phone', models.CharField(max_length=20, null=True, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('birth', models.DateField(null=True)),
                ('profile_image', models.URLField(max_length=2000, null=True)),
                ('career', models.PositiveIntegerField()),
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
        migrations.CreateModel(
            name='UploadedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_image', models.URLField()),
                ('master', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_images', to='masters.master')),
            ],
            options={
                'db_table': 'uploaded_images',
            },
        ),
    ]
