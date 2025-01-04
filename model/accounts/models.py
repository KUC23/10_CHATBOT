from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    nickname = models.CharField(max_length=150, unique=True, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^010\d{7,8}$',
                message="휴대폰 번호는 010-XXXX-XXXX 형식이어야 합니다."
            ),
        ]
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['phone_number']  


