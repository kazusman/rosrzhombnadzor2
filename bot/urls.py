from django.conf import settings
from django.urls import path

from bot.views import new_update
from bot.views import set_webhook
from bot.views import UserAPIView


urlpatterns = [
    path("set_webhook/", set_webhook),
    path(f"new_update/{settings.TELEGRAM_BOT_TOKEN}/", new_update),
    # path("api/v1/users/", UserAPIView.as_view())
]
