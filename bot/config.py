from telebot import TeleBot  # noqa
from django.conf import settings


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)
