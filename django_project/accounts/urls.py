from django.urls import path
from .views import (
    index,
    RegisterView,
    InitialSetupPage,
    login_redirect,
    login_page,
    register_page,
    chatbot_page,
)
from .views import chatbot_api
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),
    path('login-page/', login_page, name='login_page'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path("chatbot/", chatbot_page, name="chatbot_page"),
    path('redirect/', login_redirect, name='login_redirect'),
    path('register-page/', register_page, name='register_page'),
    path('api/', chatbot_api, name='chatbot_api'),
    path('', index, name='index'),
]