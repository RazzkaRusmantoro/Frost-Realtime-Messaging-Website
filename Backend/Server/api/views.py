from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login
from supabase import create_client, Client
from django.conf import settings
from .models import CustomUser

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_API_KEY
)

class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()  # Make sure to query the CustomUser model
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Check for existing user with the same email or username
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Registration unsuccessful. Username already taken."},
                            status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Registration unsuccessful. Email already in use."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Send user data to Supabase
            response = supabase.from_("users").insert(serializer.validated_data).execute()
            if response.status_code == 201:  # HTTP Created
                serializer.save()  # Save the user if everything is fine
                return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return user data

            return Response(response.data, status=response.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    def test_supabase_connection(self):
        """ Test the connection to Supabase """
        try:
            data = supabase.table('user').select('*').execute()
            if data.status_code == 200:
                return Response({"data": data.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Error fetching data from Supabase"}, status=data.status_code)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
