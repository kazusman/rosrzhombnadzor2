# Generated by Django 4.0.2 on 2022-06-21 08:22
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0034_donate_bot_message_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="Request",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "action_type",
                    models.CharField(
                        choices=[("Message", "Message"), ("Callback", "Callback")],
                        max_length=16,
                    ),
                ),
                ("data", models.JSONField(verbose_name="Data")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bot.user",
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Request",
                "verbose_name_plural": "Requests",
            },
        ),
    ]
