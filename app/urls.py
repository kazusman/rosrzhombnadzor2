from django.contrib import admin
from django.urls import path, include
from app.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bot/', include('bot.urls')),
    path('healthcheck/', health_check)
]
