from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # 자기소개
    age = models.IntegerField(blank=True, null=True)  # 나이
    gender = models.CharField(max_length=10, blank=True, null=True)  # 성별
    major = models.CharField(max_length=100, blank=True, null=True)  # 전공
    mbti = models.CharField(max_length=4, blank=True, null=True)  # MBTI