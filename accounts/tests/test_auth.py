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
    # 응답 데이터에 올바른 사용자 이름이 포함되어 있는지 확인
    assert response.data["username"] == "testuser"
    # 응답 데이터에 올바른 닉네임이 포함되어 있는지 확인
    assert response.data["nickname"] == "TestNick"

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
    # 응답 데이터에 토큰이 포함되어 있는지 확인
    assert "token" in response.data
