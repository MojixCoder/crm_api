from .models import User
from typing import Optional
from rest_framework import serializers
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class UserListSerializer(serializers.ModelSerializer):
    """ User List Serializer """
    
    url = serializers.SerializerMethodField()
    
    def get_url(self, obj) -> str:
        return obj.get_absolute_url()
    
    class Meta:
        model = User
        exclude = [
            "password", 
            "permissions", 
            "created_at", 
            "updated_at",
        ]
        

class UserRetrieveSerializer(serializers.ModelSerializer):
    """ Retrieve User Serializer """
    
    class Meta:
        model = User
        exclude = [
            "password", 
            "created_at", 
            "updated_at",
        ]
        

class UserCreateSerializer(serializers.ModelSerializer):
    """ Create User Serializer """
    
    def validate_username(self, value) -> str:
        value = value.lower()
        return value
    
    def validate_email(self, value) -> Optional[str]:
        value = value.lower() if value is not None else None
        return value
    
    def create(self, validated_data) -> User:
        password = validated_data.pop("password")
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
    
    class Meta:
        model = User
        exclude = [
            "permissions", 
            "created_at", 
            "updated_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
        

class UserUpdateSerializer(serializers.ModelSerializer):
    """ Update User Serializer """
    
    def validate_email(self, value) -> Optional[str]:
        value = value.lower() if value is not None else None
        return value
    
    class Meta:
        model = User
        exclude = [
            "username",
            "password", 
            "created_at", 
            "updated_at", 
        ]
        