from django.db import models
from accounts.models import Category

from django.db import models

class News(models.Model):
    id = models.AutoField(primary_key=True)  
    title = models.CharField(max_length=255)
    abstract = models.TextField(blank=True, null=True)
    url = models.TextField()  
    published_date = models.DateTimeField()
    category = models.ForeignKey('accounts.Category', on_delete=models.CASCADE, related_name='news')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

