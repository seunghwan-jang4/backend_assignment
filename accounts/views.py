from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import SignupSerializer, LoginSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from .permissions import IsAuthenticatedUser
import logging
import jwt
from datetime import datetime, timedelta
from rest_framework.decorators import api_view, permission_classes

logger = logging.getLogger(__name__)

User = get_user_model()

# JWT 토큰을 생성하고 검증하는 클래스
class JWTManager:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    # 토큰 생성 메소드
    def create_token(self, payload: dict, expires_delta: timedelta = None) -> str:
        to_encode = payload.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)  # 기본 30분
        
        to_encode.update({"exp": expire})
        
        return jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
    # 토큰 검증 메소드
    def verify_token(self, token: str) -> dict:
        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm]
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "username": user.username,
            "nickname": user.nickname,
            "roles": [{"role": "USER"}]
        }, status=status.HTTP_201_CREATED)
    
    logger.error(f"Signup failed: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "username": user.username,
                "nickname": user.nickname
            }, status=status.HTTP_200_OK)
    
    logger.error(f"Login failed: Invalid credentials for username {request.data.get('username')}")
    return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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
            logger.error(f"Logout failed: {str(e)}")
            return Response({"error": "잘못된 토큰"}, status=status.HTTP_400_BAD_REQUEST)

# 유저 프로필을 조회하는 뷰
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedUser]

    def get_object(self):
        return self.request.user  # 현재 인증된 사용자만 조회 가능
