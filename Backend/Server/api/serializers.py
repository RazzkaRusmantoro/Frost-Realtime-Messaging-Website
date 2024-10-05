from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):

    profile_image = serializers.CharField(required=False, allow_blank=True)  # Make optional
    biography = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "biography", "profile_image", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(**validated_data) 
        user.set_password(validated_data['password']) 
        user.save()
        return user 
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField( required = True )
    password = serializers.CharField( required = True )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Username or password incorrect")
        
        return attrs

