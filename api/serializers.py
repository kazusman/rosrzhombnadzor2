from rest_framework import serializers
from bot.models import User
from bot.models import Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'first_name', 'last_name', 'coins', 'created_at', 'date_of_birth', 'is_deleted')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("id", "user", "message_type", "is_forwarded", "created_at", "message_text", "content_hash",
                  "file_id", "message_id", "text_on_image", "recognition_type", "json_body")