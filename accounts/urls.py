from django.urls import path
from .views import SignupView, LoginView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),  # 회원가입 엔드포인트
    path('login/', LoginView.as_view(), name='login'),  # 로그인 엔드포인트
]