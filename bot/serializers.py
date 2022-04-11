from rest_framework import serializers
from bot.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'first_name', 'last_name', 'coins', 'created_at', 'date_of_birth', 'is_deleted')
