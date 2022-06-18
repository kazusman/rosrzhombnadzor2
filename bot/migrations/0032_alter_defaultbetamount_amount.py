# Generated by Django 4.0.2 on 2022-06-18 15:45

import bot.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0031_alter_defaultbetamount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultbetamount',
            name='amount',
            field=models.CharField(max_length=128, validators=[bot.models.default_amount_validator], verbose_name='Amount'),
        ),
    ]
