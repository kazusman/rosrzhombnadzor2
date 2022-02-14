# Generated by Django 4.0.2 on 2022-02-14 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0013_alter_bet_bet_target_user_alter_bet_message_and_more'),
        ('google_vision', '0002_request_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='bot.message', verbose_name='Message'),
        ),
    ]
