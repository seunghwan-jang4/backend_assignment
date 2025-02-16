from rest_framework import serializers  
from django.contrib.auth import get_user_model 
from django.contrib.auth.password_validation import validate_password

User = get_user_model()  # 현재 활성화된 사용자 모델을 User 변수에 할당

class SignupSerializer(serializers.ModelSerializer):  # 회원가입 시리얼라이저 정의
    password = serializers.CharField(write_only=True, validators=[validate_password])  # 비밀번호 필드 정의, 쓰기 전용 및 유효성 검사 추가

    class Meta:
        model = User  # 사용할 모델을 User로 설정
        fields = ('username', 'password', 'nickname')  # 시리얼라이즈할 필드 정의

    def create(self, validated_data):  # 새로운 사용자 생성 메서드
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            nickname=validated_data['nickname']
        )
        return user  # 생성된 사용자 반환

class LoginSerializer(serializers.Serializer):  # 로그인 시리얼라이저 정의
    username = serializers.CharField()  # 사용자 이름 필드 정의
    password = serializers.CharField(write_only=True)  # 비밀번호 필드 정의, 쓰기 전용

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'nickname']
