# Generated by Django 3.2.5 on 2021-07-23 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kakao_id', models.IntegerField(null=True, unique=True)),
                ('name', models.CharField(max_length=45, null=True)),
                ('password', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=20, null=True, unique=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=20, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('birth', models.DateField(null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
