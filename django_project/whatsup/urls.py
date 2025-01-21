from django.contrib import admin
from django.urls import path, include
from accounts.views import chatbot_page, friends_selection, chatbot_api, save_audio, chat_rules_view
from accounts.user_profile import profile_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include('accounts.urls')),
    path("chatbot/", chatbot_page, name='chatbot_page'),
    path('friends-selection/', friends_selection, name='friends_selection'),
    path('chatbot/api/', chatbot_api, name='chatbot_api'),  # chatbot/api 경로 직접 연결
    path('', include('main.urls')),
    path('chatbot/save-audio/', save_audio, name='save_audio'),
    
    # 프로필 페이지 추가
    path('profile/', profile_view, name='profile'),

    # Chat Rules 페이지 추가
    path('chat-rules/', chat_rules_view, name='chat_rules'),
]