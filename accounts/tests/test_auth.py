import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_signup():
    client = APIClient()
    response = client.post("/api/accounts/signup/", {
        "username": "testuser",
        "password": "testpassword123",
        "nickname": "TestNick"
    }, format="json")

    # 회원가입 요청이 성공적으로 처리되었는지 확인
    assert response.status_code == status.HTTP_201_CREATED
    # 응답 데이터에 올바른 사용자 정보가 포함되어 있는지 확인
    assert response.data["username"] == "testuser"
    assert response.data["nickname"] == "TestNick"
    assert "roles" in response.data  # roles 정보가 포함되어 있는지 확인

@pytest.mark.django_db
def test_login():
    client = APIClient()
    # 테스트 사용자 생성
    User.objects.create_user(username="testuser", password="testpassword123", nickname="TestNick")

    response = client.post("/api/accounts/login/", {
        "username": "testuser",
        "password": "testpassword123"
    }, format="json")

    # 로그인 요청이 성공적으로 처리되었는지 확인
    assert response.status_code == status.HTTP_200_OK
    # 응답 데이터에 access_token과 refresh_token이 포함되어 있는지 확인
    assert "access_token" in response.data
    assert "refresh_token" in response.data  # Refresh Token 검증 추가

@pytest.mark.django_db
def test_token_refresh():
    client = APIClient()
    # 테스트 사용자 생성
    user = User.objects.create_user(username="JIN HO", password="12341234", nickname="Mentos")

    # 로그인하여 JWT 토큰 획득
    login_response = client.post("/api/accounts/login/", {
        "username": "testuser",
        "password": "testpassword123"
    }, format="json")

    refresh_token = login_response.data["refresh_token"]

    # Refresh Token을 이용해 Access Token 갱신
    refresh_response = client.post("/api/accounts/token/refresh/", {
        "refresh": refresh_token    
    }, format="json")

    # 갱신 요청이 성공적으로 처리되었는지 확인
    assert refresh_response.status_code == status.HTTP_200_OK
    # 새 access_token이 응답 데이터에 포함되어 있는지 확인
    assert "access" in refresh_response.data
