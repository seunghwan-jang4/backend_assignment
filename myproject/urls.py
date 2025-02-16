from django.urls import path, include
from rest_framework import permissions
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
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),  # accounts 앱 URLconf 등록    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),  # Swagger UI 엔드포인트
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Django 기본 로그인 URL 추가
]
