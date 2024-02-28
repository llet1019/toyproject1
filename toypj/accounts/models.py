from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


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

    def create_superuser(self, password, email):
        try:
            user = self.model(
                password=password,
                email=email
            )
            user.is_active = True
            user.is_admin = True
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name='이름')
    is_staff = models.BooleanField(default=False, verbose_name='관계자')
    is_admin = models.BooleanField(default=False, verbose_name='관리자')
    is_superuser = models.BooleanField(default=False)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    joined_date = models.DateTimeField(auto_now_add=True, verbose_name='생성 날짜')
    login_date = models.DateTimeField(auto_now=True, verbose_name='최근 로그인')

    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = '사용자'
        ordering = ['id']

    def has_module_perms(self, app_label):
        return True

    # @property
    # def is_staff(self):
    #     return self.is_admin