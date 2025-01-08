from django.urls import path
from .views import RegisterView, InitialSetupPage, login_redirect
from django.contrib.auth.views import LoginView
from . import views
from .views import login_page
from .views import chatbot_page

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login-page/', login_page, name='login_page'),
    path('chatbot/', chatbot_page, name='chatbot_page'),
    path('redirect/', login_redirect, name='login_redirect'),
]
