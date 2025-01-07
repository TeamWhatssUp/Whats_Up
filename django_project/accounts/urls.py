from django.urls import path
from .views import RegisterView, InitialSetupPage, login_redirect
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('initial-setup-page/', InitialSetupPage.as_view(), name='initial_setup_page'),
    path('redirect/', login_redirect, name='login_redirect'),
]
