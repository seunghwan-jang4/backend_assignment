from django.urls import path
from .views import SignupView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입 엔드포인트
    path('login/', LoginView.as_view(), name='login'),  # 로그인 엔드포인트
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT 토큰 갱신 엔드포인트
]