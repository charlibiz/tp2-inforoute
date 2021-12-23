from rest_framework import fields, serializers

from django.contrib.auth.models import User
from .models import ville


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password")