from rest_framework import serializers
from .models import CustomUser
from django.db import IntegrityError

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        try:
            user = CustomUser.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email']
            )
            return user
        except IntegrityError:
            raise serializers.ValidationError({'error': 'Username or email already exists.'})

class InitialSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'gender', 'major']

class AudioUploadSerializer(serializers.Serializer):
    audio = serializers.FileField()