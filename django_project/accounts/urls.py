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
    UserLoginAPI

)
from .views import chatbot_api
from . import views

from .views import chatbot_api
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path("chatbot/", chatbot_page, name="chatbot_page"), # 챗봇 화면
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('', index, name='index'),
    path('friends-selection/', friends_selection, name='friends_selection'),  # 등장인물 선택 화면
    path('chatbot/api/', chatbot_api, name='chatbot_api'),
    path('login/', UserLoginAPI.as_view(), name='user_login'),  # 로그인 엔드포인트


]
