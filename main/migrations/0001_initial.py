# Generated by Django 4.1.1 on 2022-12-27 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Station name')),
                ('code', models.CharField(max_length=255, verbose_name='Station code')),
            ],
            options={
                'verbose_name': 'Station',
                'verbose_name_plural': 'Stations',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('tg_id', models.IntegerField(unique=True, verbose_name='Telegram ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='First name')),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name')),
                ('username', models.CharField(max_length=255, verbose_name='Username')),
                ('phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Phone number')),
                ('language_code', models.CharField(default='uz', max_length=255, verbose_name='Language code')),
            ],
            options={
                'verbose_name': 'Telegram user',
                'verbose_name_plural': 'Telegram users',
                'ordering': ['-tg_id'],
            },
        ),
        migrations.CreateModel(
            name='Train',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='Train name')),
                ('code', models.CharField(max_length=255, verbose_name='Train code')),
            ],
            options={
                'verbose_name': 'Train',
                'verbose_name_plural': 'Trains',
                'ordering': ['-id'],
            },
        ),
    ]
