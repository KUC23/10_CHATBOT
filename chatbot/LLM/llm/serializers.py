from rest_framework import serializers
from .models import Article

class Seriealizer(serializers.ModelSerializer):
    class Meta: 
        #model = 
        fields="__all__"