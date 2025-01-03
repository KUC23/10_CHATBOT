from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, Permission


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'nickname': {'required': True},
            'birthday': {'required': True},
            'phone_number': {'required': True},
            'is_active': {'required': False, 'default': True},
        }
    def validate(self, data):
        
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password": "비밀번호가 일치하지 않습니다."
            })
        return data
    
    def create(self, validated_data):
        groups = validated_data.pop('groups', [])
        user_permissions = validated_data.pop('user_permissions', [])
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password) 
        user.is_active = True  
        user.save()
        return user