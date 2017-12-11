from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from .models import Bot


class IsOwner(BasePermission):
    message = 'You must the owner of this object.'

    def has_permission(self, request, view):
        if 'bot' in view.kwargs:
            related_bot = get_object_or_404(Bot, pk=view.kwargs['bot'])
            self.message = 'You must be the owner of the bot'
            return request.user == related_bot.creator
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Bot):
            return request.user == obj.creator
        else:
            return request.user == obj.bot.creator
        