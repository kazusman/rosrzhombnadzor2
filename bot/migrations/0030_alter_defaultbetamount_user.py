# Generated by Django 4.0.2 on 2022-06-18 15:35
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0029_defaultbetamount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="defaultbetamount",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="User",
            ),
        ),
    ]
