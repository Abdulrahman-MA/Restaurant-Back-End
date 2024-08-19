from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from .serializer import UserSerializer, ResetPasswordEmailRequestSerializer
from rest_framework.views import APIView
from .models import ResetPasswordToken


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        user = authenticate(username=username, password=password, phone_number=phone_number)

        if user is not None:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
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


class PasswordResetView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = get_user_model().objects.filter(email=email).first()

        if user is not None:
            # Generate a password reset token and save it in the ResetPasswordToken model
            token = ResetPasswordToken.objects.create(user=user)

            # Send a password reset email to the user's email address
            # You can use a library like django-sendgrid or django-anymail to send the email

            return Response({"success": "Password reset email sent"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
