# Generated by Django 4.0.2 on 2022-02-11 13:31
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

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
                ("response", models.JSONField(verbose_name="Google API Response")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
            ],
            options={
                "verbose_name": "Request",
                "verbose_name_plural": "Requests",
            },
        ),
    ]
