from django.urls import path
from .views import RegisterView, InitialSetupPage, login_redirect
from django.contrib.auth.views import LoginView
from . import views
from .views import login_page, register_page, chatbot_page
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login-page/', login_page, name='login_page'),
    path('login/', TokenObtainPairView.as_view(), name='login'),  # 로그인 API
    path('chatbot/', chatbot_page, name='chatbot_page'),
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
]
