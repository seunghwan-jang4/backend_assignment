from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAuthenticatedUser


User = get_user_model()

# 회원가입을 처리하는 뷰
class SignupView(generics.CreateAPIView):  
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

# 로그인을 처리하는 뷰
class LoginView(generics.GenericAPIView):
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

# 로그아웃을 처리하는 뷰
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 로그아웃 가능

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # 토큰을 블랙리스트에 등록하여 무효화
            return Response({"message": "로그아웃 완료"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "잘못된 토큰"}, status=status.HTTP_400_BAD_REQUEST)

# 유저 프로필을 조회하는 뷰
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedUser]

    def get_object(self):
        return self.request.user  # 현재 인증된 사용자만 조회 가능


