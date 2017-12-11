from rest_framework import serializers

from users.serializers import UserDetailsSerializer
from .models import Bot, Knowledge


class BotDetailsSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = ('is_archived',)


class BotKnowledgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Knowledge
        fields = '__all__'
        read_only_fields = ('bot',)


class ArchivedBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'
        read_only_fields = (
            'name', 'description', 'category', 
            'is_active', 'tags', 'creator'
            )
