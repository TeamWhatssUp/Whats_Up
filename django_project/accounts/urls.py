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
    profile,  # profile 뷰 추가
    delete_account,  # delete_account 뷰 추가
    chatbot_api,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.views import LogoutView  # 로그아웃 뷰 추가

urlpatterns = [
    path('', index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login-page/', login_page, name='login_page'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('profile/', profile, name='profile'),  # 프로필 뷰 URL 추가
    path('delete_account/', delete_account, name='delete_account'),  # 계정 삭제 URL 추가
    path('chatbot/', chatbot_page, name='chatbot_page'),
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('friends-selection/', friends_selection, name='friends_selection'),
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃 URL 추가
]