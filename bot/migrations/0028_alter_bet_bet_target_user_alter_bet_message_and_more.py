# Generated by Django 4.0.2 on 2022-06-14 19:19
import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ("bot", "0027_message_text_from_audio_alter_user_sex"),
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
        migrations.AlterField(
            model_name="bet",
            name="message",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.message",
                verbose_name="Message",
            ),
        ),
        migrations.AlterField(
            model_name="bet",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="Bet author",
            ),
        ),
        migrations.AlterField(
            model_name="donate",
            name="from_user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="From user",
            ),
        ),
        migrations.AlterField(
            model_name="donate",
            name="to_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="to_user",
                to="bot.user",
                verbose_name="To user",
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="searchrequest",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="status",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="bot.user",
                verbose_name="User",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="coins",
            field=models.FloatField(default=3000, verbose_name="Coins"),
        ),
        migrations.CreateModel(
            name="DownloadRequest",
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
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="bot.message",
                        verbose_name="Message",
                    ),
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
                "verbose_name": "Download request",
                "verbose_name_plural": "Download requests",
            },
        ),
    ]
