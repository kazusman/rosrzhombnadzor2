# Generated by Django 4.0.2 on 2022-03-21 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0022_demotivatortext'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='content_hash',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='MD5 content hash'),
        ),
        migrations.AlterField(
            model_name='message',
            name='file_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='File ID'),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_text',
            field=models.TextField(blank=True, null=True, verbose_name='Message text'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text_on_image',
            field=models.TextField(blank=True, null=True, verbose_name='Text from image'),
        ),
    ]