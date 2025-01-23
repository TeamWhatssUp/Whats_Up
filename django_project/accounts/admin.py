from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Conversation, ChatMessage

# CustomUser 모델 등록
admin.site.register(CustomUser, UserAdmin)

# Conversation 모델 등록
admin.site.register(Conversation)

# ChatMessage 모델 등록
admin.site.register(ChatMessage)