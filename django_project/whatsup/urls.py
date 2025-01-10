from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include('accounts.urls')),  # accounts 앱의 URL 포함
]

