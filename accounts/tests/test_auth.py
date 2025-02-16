import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

@pytest.mark.django_db
def test_signup():
    client = APIClient()
    response = client.post("/api/accounts/signup/", {
        "username": "JIN HO",
        "password": "12341234",
        "nickname": "Mentos"
    }, format="json")

    # 회원가입 요청이 성공적으로 처리되었는지 확인
    assert response.status_code == status.HTTP_201_CREATED
    # 응답 데이터에 올바른 사용자 정보가 포함되어 있는지 확인
    assert response.data["username"] == "JIN HO"
    assert response.data["nickname"] == "Mentos"
    assert "roles" in response.data  # roles 정보가 포함되어 있는지 확인

@pytest.mark.django_db
def test_login():
    client = APIClient()
    # 테스트 사용자 생성
    User.objects.create_user(username="JIN HO", password="12341234", nickname="Mentos")

    response = client.post("/api/accounts/login/", {
        "username": "JIN HO",
        "password": "12341234"
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
        "username": "JIN HO",
        "password": "12341234"
    }, format="json")

    refresh_token = login_response.data["refresh_token"]

    # Refresh Token을 이용해 Access Token 갱신
    refresh_response = client.post("/api/accounts/token/refresh/", {
        "refresh": refresh_token    
    }, format="json")

    # 갱신 요청이 성공적으로 처리되었는지 확인
    assert refresh_response.status_code == status.HTTP_200_OK
    # 새 access_token이 응답 데이터에 포함되어 있는지 확인
    assert "access_token" in refresh_response.data

# 로그아웃 테스트
@pytest.mark.django_db
def test_logout():
    client = APIClient()

    # 테스트 사용자 생성 및 로그인
    user = User.objects.create_user(username="JIN HO", password="12341234", nickname="Mentos")
    login_response = client.post("/api/accounts/login/", {
        "username": "JIN HO",
        "password": "12341234"
    }, format="json")

    refresh_token = login_response.data["refresh_token"]

    # 로그아웃 요청
    response = client.post("/api/accounts/logout/", {
        "refresh": refresh_token
    }, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "로그아웃 완료"
    
# 프로필 조회 테스트
@pytest.mark.django_db
def test_user_profile_access():
    client = APIClient()
    
    # 로그인하지 않은 상태에서 프로필 조회 요청
    response = client.get("/api/accounts/profile/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED  # 인증되지 않음

    # 테스트 유저 생성 및 로그인
    user = User.objects.create_user(username="testuser", password="testpassword", nickname="Tester")
    login_response = client.post("/api/accounts/login/", {
        "username": "testuser",
        "password": "testpassword"
    }, format="json")

    access_token = login_response.data["access_token"]
    
    # 인증된 상태에서 프로필 조회 요청
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.get("/api/accounts/profile/")
    assert response.status_code == status.HTTP_200_OK  # 성공
    assert response.data["username"] == "testuser"