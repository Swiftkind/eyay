from rest_framework import serializers

from users.serializers import UserDetailsSerializer
from .models import Bot, Knowledge


class BotDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = ('creator',)


class BotKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knowledge
        fields = '__all__'