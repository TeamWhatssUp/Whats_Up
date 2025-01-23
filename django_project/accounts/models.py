from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True, null=True)  # 나이
    gender = models.CharField(max_length=10, blank=True, null=True)  # 성별
    major = models.CharField(max_length=100, blank=True, null=True)  # 전공

class ChatRules(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    introduction = models.TextField(blank=True, null=True)
    chat_rules = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Chat Rules"
