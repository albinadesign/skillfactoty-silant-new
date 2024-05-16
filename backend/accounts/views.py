from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
import logging

from .serializers import *

logger = logging.getLogger(__name__)
User = get_user_model()

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            logger.info(f"Trying to login with username: {username} and password: {'*' * len(password)}")
            if user is not None:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                logger.info("Login successful")
                return Response({
                    'message': 'Авторизация успешна',
                    'token': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                logger.warning("Login failed")
                return Response({'error': 'Неправильный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        logger.error(f"Validation failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    

class CheckAuthStatusAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        is_authenticated = request.user.is_authenticated
        if is_authenticated:
            user_info = {
                'is_authenticated': True,
                'username': request.user.username
            }
            logger.info(f"User {request.user.username} is authenticated.")
        else:
            user_info = {'is_authenticated': False}
            logger.info("User is not authenticated.")
        return Response(user_info)
    
    
class UserDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

