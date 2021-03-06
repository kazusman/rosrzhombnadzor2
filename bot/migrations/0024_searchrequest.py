# Generated by Django 4.0.2 on 2022-03-22 08:23
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0023_alter_message_content_hash_alter_message_file_id_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SearchRequest",
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
                ("search_text", models.TextField(verbose_name="Search text")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Search text"),
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
                "verbose_name": "Search request",
                "verbose_name_plural": "Search requests",
            },
        ),
    ]
