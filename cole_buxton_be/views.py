from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

# Create your views here.
class RegisterView(APIView):
  def post(self, request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')

    if password != password_confirm:
      return Response({'error': 'Passwords do not match.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
      return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(email=email).exists():
      return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User(
      username=username,
      email=email,
      password=make_password(password)
    )
    user.save()

    return Response({}, status=status.HTTP_201_CREATED)
