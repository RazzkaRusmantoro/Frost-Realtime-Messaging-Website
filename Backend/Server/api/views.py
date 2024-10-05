from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()    
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        