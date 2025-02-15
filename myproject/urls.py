"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version="v1",
        description="API Documentation",
    ),
    public=True,
)

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),  # accounts 앱 URLconf 등록    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI 엔드포인트
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Django 기본 로그인 URL 추가
]
