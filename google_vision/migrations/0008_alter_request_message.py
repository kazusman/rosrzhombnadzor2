# Generated by Django 4.0.2 on 2022-05-26 08:06
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0026_user_sex_alter_bet_bet_target_user_alter_bet_message_and_more"),
        ("google_vision", "0007_alter_recognitiontype_is_main"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="message",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="bot.message",
                verbose_name="Message",
            ),
        ),
    ]
