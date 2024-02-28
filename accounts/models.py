from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, name, password, email):
        try:
            user = self.model(
                name=name,
                password=password,
                email=email
            )
            user.is_active = True
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)

    def create_superuser(self, name, password, email):
        try:
            user = self.model(
                name=name,
                password=password,
                email=email
            )
            user.is_active = True
            user.is_admin = True
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, verbose_name='이메일 주소')
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='이름')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    joined_date = models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')
    login_date = models.DateTimeField(auto_now=True, verbose_name='최근 로그인')

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
        ordering = ['id']