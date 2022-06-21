from django.conf import settings
from telebot import TeleBot  # noqa
from minio import Minio


bot = TeleBot(settings.TELEGRAM_BOT_TOKEN)

minio = Minio(f"minio:{settings.MINIO_API_PORT}", access_key=settings.MINIO_ACCESS_KEY,
              secret_key=settings.MINIO_SECRET_KEY, secure=False)

