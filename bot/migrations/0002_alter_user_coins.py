# Generated by Django 4.0.2 on 2022-02-11 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='coins',
            field=models.FloatField(default=10000, verbose_name='Coins'),
        ),
    ]
