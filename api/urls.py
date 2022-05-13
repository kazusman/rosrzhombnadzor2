from django.urls import path

from api.views import MessageAPIView
from api.views import UserAPIView


urlpatterns = [
    path("users/", UserAPIView.as_view()),
    path("messages/", MessageAPIView.as_view()),
]
