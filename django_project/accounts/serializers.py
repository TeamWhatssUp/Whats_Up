from rest_framework import serializers
from .models import CustomUser
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # 필요한 필드만 나열
