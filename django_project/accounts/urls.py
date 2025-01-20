from django.urls import path
from .views import (
    index,
    RegisterView,
    InitialSetupPage,
    login_redirect,
    login_page,
    register_page,
    chatbot_page,
    friends_selection,
    chatbot_api,
    UserLoginAPI,
    profile_view  # 추가
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("chatbot/", chatbot_page, name="chatbot_page"),
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('', index, name='index'),
    path('friends-selection/', friends_selection, name='friends_selection'),
    path('chatbot/api/', chatbot_api, name='chatbot_api'),
    path('login/', UserLoginAPI.as_view(), name='user_login'),
    path('profile/', profile_view, name='profile'),  # 프로필 페이지 추가
    path('delete-account/', profile_view, name='delete_account'),  # 회원 탈퇴 URL 추가

    # Django 기본 제공 기능 추가
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='profile.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='profile.html'), name='password_change_done'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # 로그인 페이지 추가
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]
