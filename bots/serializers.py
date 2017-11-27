from rest_framework import serializers

from users.serializers import UserDetailsSerializer
from .models import Bot


class BotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = ('creator',)
