from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from .serializers import UserDetailsSerializer


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class UserProfile(ViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserDetailsSerializer

    def get(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(self.request.user)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = UserDetailsSerializer(self.request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
