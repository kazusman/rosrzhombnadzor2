# Generated by Django 4.0.2 on 2022-06-21 17:41
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0035_request"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="permanent_nickname",
            field=models.CharField(
                default=models.CharField(
                    blank=True, max_length=32, null=True, verbose_name="Username"
                ),
                max_length=64,
                verbose_name="Permanent nickname",
            ),
        ),
    ]
