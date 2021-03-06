# Generated by Django 4.0.2 on 2022-02-12 12:35
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0010_user_is_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bet",
            name="bet_target_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="target_bet_user",
                to="bot.user",
                verbose_name="Bet target user",
            ),
        ),
    ]
