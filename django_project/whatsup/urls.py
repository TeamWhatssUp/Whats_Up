from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from accounts.views import (
    chatbot_page, 
    friends_selection, 
    chatbot_api, 
    save_audio, 
    save_conversation, 
    get_conversations, 
    chat_history,
)

from accounts.chat_rules import chat_rules_view, save_chat_rules  # chat_rules.py에서 직접 불러오기
from accounts.user_profile import profile_view
from accounts import views as accounts_views  # accounts의 views를 accounts_views로 임포트

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 계정 관련 URL 포함
    path("account/", include('accounts.urls')),

    # 챗봇 관련 URL
    path("chatbot/", chatbot_page, name='chatbot_page'),
    path("chatbot/api/", chatbot_api, name='chatbot_api'),
    path("chatbot/save-audio/", save_audio, name='save_audio'),

    # 친구 선택 페이지
    path('friends-selection/', friends_selection, name='friends_selection'),

    # Chat Rules 페이지 추가
    path('chat-rules/', chat_rules_view, name='chat_rules'),
    path('save-chat-rules/', save_chat_rules, name='save_chat_rules'),

    # 프로필 관련 URL
    path('profile/', profile_view, name='profile'),

    # main 앱 URL 포함 (기본 홈페이지 연결)
    path('', include('main.urls')),

    path('saved/', chat_history, name='chat_history'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

