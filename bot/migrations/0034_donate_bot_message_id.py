# Generated by Django 4.0.2 on 2022-06-18 17:25
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0033_defaultdonateamount"),
    ]

    operations = [
        migrations.AddField(
            model_name="donate",
            name="bot_message_id",
            field=models.IntegerField(
                blank=True, null=True, verbose_name="Bot message id"
            ),
        ),
    ]
