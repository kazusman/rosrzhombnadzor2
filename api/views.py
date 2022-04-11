from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from bot.models import User
from bot.models import Message
from api.serializers import UserSerializer
from api.serializers import MessageSerializer


class UserAPIView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


class MessageAPIView(generics.ListAPIView):

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
