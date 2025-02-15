from django.contrib.auth.models import AbstractUser  # Django의 기본 사용자 모델을 확장하기 위해 가져옴
from django.db import models  

class CustomUser(AbstractUser):  # AbstractUser를 상속받아 사용자 모델을 커스터마이징
    nickname = models.CharField(max_length=30, unique=True)  # 사용자에게 고유한 닉네임을 부여하는 추가 필드
