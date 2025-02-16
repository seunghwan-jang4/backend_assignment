import pytest
from django.test import TestCase
import jwt
from datetime import datetime, timedelta
from accounts.views import JWTManager  # JWTManager 클래스를 import

# 테스트 실행
# pytest accounts/tests.py -v 

# JWTManager 클래스 테스트
class TestJWTToken(TestCase):
    def setUp(self):
        self.secret_key = "your-secret-key"
        self.algorithm = "HS256"
        self.jwt_manager = JWTManager(self.secret_key, self.algorithm)
        self.test_payload = {
            "user_id": 1,
            "username": "testuser"
        }
    # 토큰 생성 테스트
    def test_create_access_token(self):
        # Given: 토큰 생성을 위한 페이로드와 만료시간 설정
        expires_delta = timedelta(minutes=30)
        
        # When: 토큰 생성
        token = self.jwt_manager.create_token(
            payload=self.test_payload, 
            expires_delta=expires_delta
        )
        
        # Then: 토큰이 문자열이며 디코딩 가능한지 확인
        assert isinstance(token, str)
        decoded = jwt.decode(
            token, 
            self.secret_key, 
            algorithms=[self.algorithm]
        )
        assert decoded["user_id"] == self.test_payload["user_id"]
        assert decoded["username"] == self.test_payload["username"]

    # 리프레시 토큰 생성 테스트
    def test_create_refresh_token(self):
        """Refresh 토큰 생성 테스트"""
        # Given: 리프레시 토큰을 위한 긴 만료시간 설정
        expires_delta = timedelta(days=14)
        
        # When: 토큰 생성
        token = self.jwt_manager.create_token(
            payload=self.test_payload, 
            expires_delta=expires_delta
        )
        
        # Then: 토큰 검증
        decoded = jwt.decode(
            token, 
            self.secret_key, 
            algorithms=[self.algorithm]
        )
        assert "exp" in decoded
        exp_datetime = datetime.fromtimestamp(decoded["exp"])
        assert exp_datetime > datetime.utcnow() + timedelta(days=13)

    # 유효한 토큰 검증 테스트
    def test_verify_valid_token(self):
        """유효한 토큰 검증 테스트"""
        # Given: 유효한 토큰 생성
        token = self.jwt_manager.create_token(self.test_payload)
        
        # When: 토큰 검증
        decoded = self.jwt_manager.verify_token(token)
        
        # Then: 페이로드 확인
        assert decoded["user_id"] == self.test_payload["user_id"]
        assert decoded["username"] == self.test_payload["username"]
        
    # 토큰 만료 검증 테스트
    def test_verify_expired_token(self):
        # Given: 즉시 만료되는 토큰 생성
        expires_delta = timedelta(seconds=-1)
        token = self.jwt_manager.create_token(
            payload=self.test_payload,
            expires_delta=expires_delta
        )
        # When & Then: 만료된 토큰 검증 시 예외 발생 확인
        with pytest.raises(jwt.ExpiredSignatureError):
            self.jwt_manager.verify_token(token)
            
    # 토큰 검증 실패 테스트
    def test_verify_invalid_token(self):
        # Given: 잘못된 토큰
        invalid_token = "invalid.token.string"
        
        # When & Then: 잘못된 토큰 검증 시 예외 발생 확인
        with pytest.raises(jwt.InvalidTokenError):
            self.jwt_manager.verify_token(invalid_token)