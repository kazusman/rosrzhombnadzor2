# Generated by Django 4.0.2 on 2022-02-24 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0019_alter_funnyaction_answer_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=True, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user', verbose_name='From user')),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to='bot.user', verbose_name='To user')),
            ],
            options={
                'verbose_name': 'Donate',
                'verbose_name_plural': 'Donates',
            },
        ),
    ]