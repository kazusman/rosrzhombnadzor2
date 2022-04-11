from api.views import UserAPIView
from api.views import MessageAPIView
from django.urls import path


urlpatterns = [
    path("users/", UserAPIView.as_view()),
    path("messages/", MessageAPIView.as_view())
]