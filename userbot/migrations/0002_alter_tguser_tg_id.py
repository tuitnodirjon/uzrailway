# Generated by Django 4.1.1 on 2023-01-08 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userbot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tguser',
            name='tg_id',
            field=models.BigIntegerField(),
        ),
    ]