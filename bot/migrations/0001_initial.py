# Generated by Django 4.0.2 on 2022-02-11 11:01
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                    "telegram_id",
                    models.BigIntegerField(unique=True, verbose_name="Telegram ID"),
                ),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=32, null=True, verbose_name="Username"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="First name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=64, null=True, verbose_name="Last name"
                    ),
                ),
                ("coins", models.FloatField(verbose_name="Coins")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "date_of_birth",
                    models.DateField(
                        blank=True, null=True, verbose_name="Date of birth"
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
            },
        ),
        migrations.CreateModel(
            name="Status",
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
                ("status", models.CharField(max_length=64, verbose_name="Status")),
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
                "verbose_name": "Status",
                "verbose_name_plural": "Statuses",
            },
        ),
    ]
