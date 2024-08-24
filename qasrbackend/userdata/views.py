from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Users, ResetPasswordToken, Order, OrderHistory, Payment, Profile
from .serializer import (
    UserSerializer, ResetPasswordTokenSerializer, OrderSerializer,
    OrderHistorySerializer, PaymentSerializer, ProfileSerializer
)


@swagger_auto_schema(
    method='POST',
    operation_description="Retrieve users from the Database.",
    responses={200: UserSerializer(many=True)}
)
@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'Bad Request', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='POST',
    operation_description="Retrieve users from the Database.",
    request_body=UserSerializer,
    responses={200: UserSerializer(many=True)}
)
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = Users.objects.filter(email=email).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Applying the description on the UserViews
@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve users from the Database.",
    responses={200: UserSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_create(request):
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, status.HTTP_302_FOUND)


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve a specific user from the Database.and requires the Email",
    responses={200: UserSerializer(many=True)}
)
# Applying the requirements,description on the Views
@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail(request, pk):
    try:
        user = Users.objects.get(pk=pk)
    except Users.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# Reset Password Token
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def reset_password_token_list_create(request):
    if request.method == 'GET':
        tokens = ResetPasswordToken.objects.all()
        serializer = ResetPasswordTokenSerializer(tokens, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = ResetPasswordTokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def reset_password_token_detail(request, pk):
    try:
        token = ResetPasswordToken.objects.get(pk=pk)
    except ResetPasswordToken.DoesNotExist:
        return JsonResponse({'error': 'Reset Password Token not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResetPasswordTokenSerializer(token)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = ResetPasswordTokenSerializer(token, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        token.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# Order
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_list_create(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# Order History
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def order_history_list_create(request):
    if request.method == 'GET':
        order_histories = OrderHistory.objects.all()
        serializer = OrderHistorySerializer(order_histories, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = OrderHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def order_history_detail(request, pk):
    try:
        order_history = OrderHistory.objects.get(pk=pk)
    except OrderHistory.DoesNotExist:
        return JsonResponse({'error': 'Order History not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderHistorySerializer(order_history)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = OrderHistorySerializer(order_history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order_history.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# Payment
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_list_create(request):
    if request.method == 'GET':
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_detail(request, pk):
    try:
        payment = Payment.objects.get(pk=pk)
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PaymentSerializer(payment)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = PaymentSerializer(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        payment.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


# Profile
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_list_create(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return JsonResponse(serializer.data)

    elif request.method == 'POST':
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile_detail(request, pk):
    try:
        profile = Profile.objects.get(pk=pk)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return JsonResponse(serializer.data)

    elif request.method == 'PATCH':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        profile.delete()
        return JsonResponse({'error': 'No Content'}, status=status.HTTP_204_NO_CONTENT)
    return JsonResponse({'error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)
