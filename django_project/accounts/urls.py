from django.urls import path
from .views import (
    index,
    RegisterView,
    InitialSetupPage,
    login_redirect,
    register_page,
    chatbot_page,
    friends_selection,
    chatbot_api,
    chat_history,
    UserLoginAPI,
    profile_view,
    logout_view, 
    delete_account_view,
    CustomPasswordChangeView,

    profile_view,  # 프로필 페이지 추가
    get_conversations,
    save_conversation,
    clear_chat_history,  # 이 줄 추가
)
from django.contrib.auth import views as auth_views
from accounts.chat_rules import chat_rules_view, save_chat_rules
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("chatbot/", chatbot_page, name="chatbot_page"),
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('', index, name='index'),
    path('friends-selection/', friends_selection, name='friends_selection'),
    path('chatbot/api/', chatbot_api, name='chatbot_api'),
    path('saved/', chat_history, name='chat_history'),  # 채팅 기록 조회 경로 추가
    
    path('profile/', profile_view, name='profile'),  # 프로필 페이지 추가
    path('chat-rules/', chat_rules_view, name='chat_rules'),  # Chat Rules 페이지 추가
    path('save-chat-rules/', save_chat_rules, name='save_chat_rules'),  # 데이터 저장 URL 추가
    # CustomPasswordChangeView와 연결
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('login/', UserLoginAPI.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('delete-account/', delete_account_view, name='delete_account'),
    

    path('clear-chat/', clear_chat_history, name='clear_chat_history'),  # 채팅 기록 초기화 경로 추가
]