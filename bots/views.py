from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN
)

from .models import Bot
from .serializers import BotDetailsSerializer 


class BotViewSet(ViewSet):
    queryset = Bot.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BotDetailsSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        kwargs['context'] = {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }
        return serializer_class(*args, **kwargs)

    def list(self, request):
        user_bots = Bot.objects.filter(creator=self.request.user)
        serializer = BotDetailsSerializer(user_bots, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = BotDetailsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(creator=self.request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        instance = get_object_or_404(Bot, pk=pk)
        if self.request.user != instance.creator:
            return Response(None, status=HTTP_403_FORBIDDEN)
        serializer = BotDetailsSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        instance = get_object_or_404(Bot, pk=pk)
        if self.request.user == instance.creator:
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(None, status=HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        if self.request.user == instance.creator:
            instance = get_object_or_404(Bot, pk=pk)
            instance.delete()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(None, status=HTTP_403_FORBIDDEN)
