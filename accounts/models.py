from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# 사용자 매니저 정의
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('사용자명은 필수입니다')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

# 사용자 모델 정의
class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=30, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nickname']  # 필수 필드 추가

    objects = CustomUserManager()

    def __str__(self):
        return self.username  # 사용자명 반환