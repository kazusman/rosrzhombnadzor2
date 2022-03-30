# Generated by Django 4.0.2 on 2022-02-15 11:18
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0014_alter_bet_bet_target_user_alter_bet_message_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Anekdot",
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
                ("anek", models.TextField(unique=True, verbose_name="Anekdot")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
            ],
            options={
                "verbose_name": "Anekdot",
                "verbose_name_plural": "Anekdots",
            },
        ),
    ]
