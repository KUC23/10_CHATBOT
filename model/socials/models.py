from django.db import models
from accounts.models import User 

class CustomSocialAccount(models.Model):  
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_social_accounts"
    )
    provider = models.CharField(max_length=50)
    uid = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} - {self.user.username}"


