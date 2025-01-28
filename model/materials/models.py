from django.db import models
from accounts.models import Category, User

class Vocabulary(models.Model):
    word = models.JSONField(default=dict, blank=True, unique=True)  # 단어는 고유값으로 관리

    def __str__(self):
        return self.word

class News(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)  
    abstract = models.TextField(blank=True, null=True)  
    summary_english = models.TextField(blank=True, null=True) 
    summary_korean = models.TextField(blank=True, null=True)  
    vocab = models.ManyToManyField(Vocabulary,related_name='news_vocab')
    url = models.TextField(unique=True)  
    category = models.ForeignKey('accounts.Category', on_delete=models.CASCADE, related_name='news') 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



