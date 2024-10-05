from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    profile_image = serializers.CharField(required=False, allow_blank=True)  # Make optional
    biography = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "biography", "profile_image", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        required_fields = ['email', 'username', 'password']
        errors = {}

        for field in required_fields:
            if field not in data or not data[field].strip():
                errors[field] = f"{field.replace('_', ' ').capitalize()} is required."

        if 'email' in data:
            if CustomUser.objects.filter(email=data['email']).exists():
                errors['email'] = _("Email already exists.")

        if 'username' in data:
            if CustomUser.objects.filter(username=data['username']).exists():
                errors['username'] = _("This username is already taken.")

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user 

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Username or password incorrect")
        
        return attrs
