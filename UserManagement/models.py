from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from .user_manager import userManager


class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name='username',
        max_length=50,
        blank=True, null=True,unique=True
    )
    email = models.CharField(max_length=200,unique=True)
    password = models.CharField(max_length=20)
    new_password = models.CharField(max_length=20)
    otp = models.CharField(max_length=4)
    is_verified = models.BooleanField(default=False)
    reset_pass = models.CharField(max_length=20)
    objects = userManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email