# Generated by Django 4.0.2 on 2022-02-11 14:51
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0006_alter_message_message_type"),
        ("google_vision", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
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
