from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
    )
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST
    )

from .models import Bot
from .serializers import BotDetailsSerializer 
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
