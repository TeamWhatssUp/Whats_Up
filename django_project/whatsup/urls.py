from django.contrib import admin
from django.urls import path, include
from accounts.views import chatbot_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include('accounts.urls')),
    path('chatbot/', chatbot_page, name='chatbot_page'),
    
]
