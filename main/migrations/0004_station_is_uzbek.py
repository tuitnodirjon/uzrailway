# Generated by Django 4.1.1 on 2022-12-27 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_rename_stations_station'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='is_uzbek',
            field=models.BooleanField(default=False),
        ),
    ]