from django.urls import path
from .views import (
    index,
    RegisterView,
    login_redirect,
    login_page,
    chatbot_page,
    friends_selection,
    chatbot_api,
)
from .profile import profile_view, logout_view  # profile.py에서 함수 가져오기
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 회원가입 및 로그인 관련 경로
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # JWT 로그인
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 토큰 갱신
    path('login-page/', login_page, name='login_page'),  # HTML 로그인 페이지

    # 프로필 및 로그아웃
    path('profile/', profile_view, name='profile'),  # 사용자 프로필 보기/수정
    path('logout/', logout_view, name='logout'),  # 로그아웃 처리

    # 기타 기능 관련 경로
    path('friends-selection/', friends_selection, name='friends_selection'),  # 등장인물 선택 화면
    path('chatbot/', chatbot_page, name='chatbot_page'),  # 챗봇 화면
    path('chatbot/api/', chatbot_api, name='chatbot_api'),  # 챗봇 API

    # 기본 및 기타 경로
    path('redirect/', login_redirect, name='login_redirect'),
    path('api/', chatbot_api, name='chatbot_api'),  # 중복 제거 가능
    path('', index, name='index'),  # 기본 경로
]

