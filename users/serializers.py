from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model without username and password
    """
    class Meta:
        model = get_user_model()
        fields = ('pk', 'email', 'first_name', 'last_name')
        read_only_fields = ('email',)
 