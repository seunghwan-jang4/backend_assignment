import pytest
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

# Create your tests here.
@pytest.mark.django_db
def test_signup():
    client = Client()  # 테스트 클라이언트 인스턴스 생성
    response = client.post('/accounts/signup/', {  # 회원가입 API 엔드포인트에 POST 요청
        'username': 'JIN HO',
        'password': '12341234',
        'nickname': 'Mentos'
    })
    assert response.status_code == 201  # 응답 상태 코드가 201(Created)인지 확인

@pytest.mark.django_db
def test_login():
    client = Client()  # 테스트 클라이언트 인스턴스 생성
    client.post('/accounts/signup/', {  # 회원가입 API 엔드포인트에 POST 요청
        'username': 'JIN HO',
        'password': '12341234',
        'nickname': 'Mentos'
    })
    response = client.post('/accounts/login/', {  # 로그인 API 엔드포인트에 POST 요청
        'username': 'JIN HO',
        'password': '12341234'
    })
    assert response.status_code == 200  # 응답 상태 코드가 200(OK)인지 확인
    assert 'token' in response.data  # 응답 데이터에 토큰이 포함되어 있는지 확인

def test_token():
    refresh = RefreshToken.for_user(user)  # 주어진 사용자에 대해 새 리프레시 토큰 생성
    assert refresh.access_token is not None  # 액세스 토큰이 None이 아닌지 확인

@pytest.mark.django_db
def test_jwt():
    user = User.objects.create_user(username='testuser', password='12345')  # 새로운 사용자 생성
    refresh = RefreshToken.for_user(user)  # 생성된 사용자에 대해 새 리프레시 토큰 생성
    assert refresh.access_token is not None  # 액세스 토큰이 None이 아닌지 확인