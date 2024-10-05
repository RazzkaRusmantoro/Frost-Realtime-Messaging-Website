from .models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "biography", "profile_image", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data) 
        user.set_password(validated_data['password']) 
        user.save()
        return user 
