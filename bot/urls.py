from django.urls import path
from bot.views import set_webhook, new_update
from django.conf import settings


urlpatterns = [
    path('set_webhook/', set_webhook),
    path(f'new_update/{settings.TELEGRAM_BOT_TOKEN}/', new_update)
]
