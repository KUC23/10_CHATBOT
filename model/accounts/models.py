from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False)  
    last_name = models.CharField(max_length=150, blank=False)
    nickname = models.CharField(max_length=150, unique=True) 
    birthday = models.DateField()  
    gender = models.CharField(max_length=10, blank=True, null=True) 
    introduction = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
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
