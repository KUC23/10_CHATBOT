from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import Serializer, CharField
from django.contrib.auth import authenticate

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    user_permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'nickname': {'required': False},
            'birthday': {'required': False},
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

class DeleteAccountSerializer(Serializer):
    password = CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        if not authenticate(username=user.username, password=data['password']):
            raise serializers.ValidationError({"password": "비밀번호가 올바르지 않습니다."})
        return data
    
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'nickname', 'birthday', 'phone_number']

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({"new_password": "비밀번호가 일치하지 않습니다."})
        return data

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user