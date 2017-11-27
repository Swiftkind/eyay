from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
    )
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
    )

from .models import Bot, Knowledge
from .serializers import BotDetailsSerializer, BotKnowledgeSerializer
from .permissions import IsOwnerOrAdmin



class BotListCreateView(ListCreateAPIView):
    queryset = Bot.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BotDetailsSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(creator=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(is_active=True, creator=self.request.user)


class BotRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Bot.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    serializer_class = BotDetailsSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(creator=self.request.user)
        instance = self.get_object()
        serializer = BotDetailsSerializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BotDetailsSerializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=HTTP_200_OK)


class KnowledgeListCreateView(ListCreateAPIView):
    queryset = Knowledge.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BotKnowledgeSerializer

    """
    This view should return a list of all knowledge of
    the specific bot passed in the URL
    """
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(bot=self.kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        specificbot = Bot.objects.filter(id=self.kwargs['pk'])
        if specificbot.exists():
            serializer.save(bot=specificbot.first())
        else:
            return Response(None, status=HTTP_404_NOT_FOUND)


class KnowledgeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Knowledge.objects.all()
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    serializer_class = BotKnowledgeSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(pk=self.kwargs['pk'])
        instance = self.get_object()
        serializer = BotKnowledgeSerializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BotKnowledgeSerializer(instance, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=HTTP_200_OK)
