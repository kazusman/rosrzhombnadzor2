# Generated by Django 4.0.2 on 2022-06-21 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0036_user_permanent_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permanent_nickname',
            field=models.CharField(max_length=64, null=True, verbose_name='Permanent nickname'),
        ),
    ]