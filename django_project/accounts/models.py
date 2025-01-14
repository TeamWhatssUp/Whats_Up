from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True, null=True)  # 나이
    gender = models.CharField(max_length=10, blank=True, null=True)  # 성별
    major = models.CharField(max_length=100, blank=True, null=True)  # 전공