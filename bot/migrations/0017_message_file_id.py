# Generated by Django 4.0.2 on 2022-02-23 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_bet_declined_at_bet_is_declined'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_id',
            field=models.CharField(max_length=128, null=True, verbose_name='File ID'),
        ),
    ]
