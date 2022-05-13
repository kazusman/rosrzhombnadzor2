from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.serializers import MessageSerializer
from api.serializers import UserSerializer
from bot.models import Message
from bot.models import User


class UserAPIView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class MessageAPIView(generics.ListAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
