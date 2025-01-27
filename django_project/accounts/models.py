from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

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

    
User = get_user_model()

class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'conversations'

    def __str__(self):
        return f"{self.user.username}의 대화 ({self.created_at})"

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 사용자와의 관계
    character = models.CharField(max_length=100)  # 캐릭터 이름
    message = models.TextField()  # 사용자 메시지 내용
    response = models.TextField(null=True, blank=True)  # 챗봇 응답 내용
    timestamp = models.DateTimeField(auto_now_add=True)  # 메시지 전송 시간

    def __str__(self):
        return f"{self.user.username}: {self.message[:20]}..."  # 메시지 미리보기

