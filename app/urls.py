from django.contrib import admin
from django.urls import include
from django.urls import path

from app.views import health_check
from app.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bot/", include("bot.urls")),
    path("healthcheck/", health_check),
    path("", index)
]
