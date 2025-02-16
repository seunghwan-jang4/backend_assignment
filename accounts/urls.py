from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # 회원가입 URL
    path('login/', views.login, name='login'),  # 로그인 URL
    path('logout/', views.LogoutView.as_view(), name='logout'),  # 로그아웃 URL
    path('profile/', views.UserProfileView.as_view(), name='profile'),  # 프로필 조회 URL
    path('token/create/', views.create_token, name='create_token'),  # 토큰 생성 URL
    path('token/verify/', views.verify_token, name='verify_token'),  # 토큰 검증 URL
]