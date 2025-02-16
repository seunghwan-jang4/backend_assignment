from django.urls import path
from .views import SignupView, LoginView, LogoutView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입 엔드포인트
    path('login/', LoginView.as_view(), name='login'),  # 로그인 엔드포인트
    path('logout/', LogoutView.as_view(), name='logout'),  # 로그아웃 엔드포인트 추가
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT 토큰 갱신 엔드포인트
    path('profile/', UserProfileView.as_view(), name='user-profile'),  # 프로필 조회 API 추가
]
