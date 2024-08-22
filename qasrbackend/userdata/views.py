
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializer import UserSerializer, ResetPasswordEmailRequestSerializer, EmailChangeSerializer
from .models import ResetPasswordToken
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
def get_all_users(request):
    try:
        users = User.objects.all()  # Make sure 'User' is singular if using the default Django User model
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)  # Use Response instead of JsonResponse
    except Exception as e:
        print(f'Error: {e}')
        return JsonResponse({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request, *args, **kwargs):
    try:
        # Extract username and password from request data
        email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(email=email, password=password)

        if user is not None:
            # Serialize the user data if authentication is successful
            serializer = UserSerializer(user)
            return JsonResponse(serializer.data, safe=False)
        else:
            # Return an error response if credentials are invalid
            return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        # Log the exception and return a generic error response
        print(f'Error: {e}')
        return JsonResponse({"error": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def signup(request, *args, **kwargs):
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