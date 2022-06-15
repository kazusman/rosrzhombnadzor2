# Generated by Django 4.0.2 on 2022-06-14 19:19
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0028_alter_bet_bet_target_user_alter_bet_message_and_more"),
        ("google_vision", "0008_alter_request_message"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="message",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.message",
                verbose_name="Message",
            ),
        ),
    ]
