import pytest
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
@pytest.mark.django_db
def test_signup():
    client = Client()
    response = client.post('/accounts/signup/', {
        'username': 'JIN HO',
        'password': '12341234',
        'nickname': 'Mentos'
    })
    assert response.status_code == 201

@pytest.mark.django_db
def test_login():
    client = Client()
    client.post('/accounts/signup/', {
        'username': 'JIN HO',
        'password': '12341234',
        'nickname': 'Mentos'
    })
    response = client.post('/accounts/login/', {
        'username': 'JIN HO',
        'password': '12341234'
    })
    assert response.status_code == 200
    assert 'token' in response.data

def test_token():
    refresh = RefreshToken.for_user(user)
    assert refresh.access_token is not None

@pytest.mark.django_db
def test_jwt():
    user = User.objects.create_user(username='testuser', password='12345')
    refresh = RefreshToken.for_user(user)
    assert refresh.access_token is not None