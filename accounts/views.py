from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupView(generics.CreateAPIView):  # 회원가입을 처리하는 뷰
    queryset = User.objects.all()
    serializer_class = SignupSerializer

    def post(self, request, *args, **kwargs):  # 회원가입 요청을 처리하는 메서드
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # 시리얼라이저가 유효한 경우
            user = serializer.save()  # 사용자 저장
            return Response({
                "username": user.username,
                "nickname": user.nickname,
                "roles": [{"role": "USER"}]
            }, status=status.HTTP_201_CREATED)  # 성공 응답 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 오류 응답 반환

class LoginView(generics.GenericAPIView):  # 로그인을 처리하는 뷰
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):  # 로그인 요청을 처리하는 메서드
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():  # 시리얼라이저가 유효한 경우
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)  # 사용자 인증

            if user:  # 인증된 사용자인 경우
                refresh = RefreshToken.for_user(user)  # JWT 리프레시 토큰 생성
                return Response({
                    "access_token": str(refresh.access_token),  # Access Token 반환
                    "refresh_token": str(refresh)  # Refresh Token 반환
                }, status=status.HTTP_200_OK)  # 성공 응답 반환

        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)  # 오류 응답 반환
