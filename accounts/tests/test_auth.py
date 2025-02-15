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

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["username"] == "testuser"
    assert response.data["nickname"] == "TestNick"

@pytest.mark.django_db
def test_login():
    client = APIClient()
    User.objects.create_user(username="testuser", password="testpassword123", nickname="TestNick")

    response = client.post("/api/accounts/login/", {
        "username": "testuser",
        "password": "testpassword123"
    }, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data
