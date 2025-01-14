from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # 관리자 페이지
    path("account/", include('accounts.urls')),  # accounts 앱의 URL 연결
]