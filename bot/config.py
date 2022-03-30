from django.conf import settings
from telebot import TeleBot  # noqa


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)
