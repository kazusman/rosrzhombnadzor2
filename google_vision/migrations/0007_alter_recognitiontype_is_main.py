# Generated by Django 4.0.2 on 2022-03-18 19:19
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("google_vision", "0006_alter_recognitiontype_is_main"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recognitiontype",
            name="is_main",
            field=models.BooleanField(
                choices=[(True, "✅ Yes"), (False, "❌ No")],
                default=False,
                verbose_name="Is main?",
            ),
        ),
    ]
