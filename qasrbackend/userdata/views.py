from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from .serializer import UserSerializer, ResetPasswordEmailRequestSerializer, EmailChangeSerializer
from .models import ResetPasswordToken
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

@api_view(['GET'])
def login(self, request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    phone_number = request.data.get('phone_number')
    user = authenticate(username=username, password=password, phone_number=phone_number)

    if user is not None:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup(self, request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')

    if not username or not password or not email or not phone_number:
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = get_user_model().objects.create_user(username=username, password=password,
                                                    email=email, phone_number=phone_number)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
def reset_password(request):
    serializer_class = ResetPasswordEmailRequestSerializer
    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    user = get_user_model().objects.filter(email=email).first()

    if user is not None:
        token = ResetPasswordToken.objects.create(user=user)

        return Response({"success": "Password reset email sent"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@login_required
@api_view(['PATCH'])
def change_email(request):
    serializer = EmailChangeSerializer(data=request.data)
    if serializer.is_valid():
        new_email = serializer.validated_data['new_email']
        request.user.email = new_email
        request.user.save()
        return Response({'detail': 'Email updated successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)