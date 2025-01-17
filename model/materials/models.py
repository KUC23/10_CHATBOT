from django.db import models
from accounts.models import Category

class News(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)  
    abstract = models.TextField(blank=True, null=True)  
    summary_english = models.TextField(blank=True, null=True) 
    summary_korean = models.TextField(blank=True, null=True)  
    vocab = models.JSONField(default=dict, blank=True)  
    url = models.TextField(unique=True)  
    category = models.ForeignKey('accounts.Category', on_delete=models.CASCADE, related_name='news') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



