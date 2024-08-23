from rest_framework import serializers
from .models import Users, ResetPasswordToken, Order, OrderHistory, Payment, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_id', 'username', 'email', 'phone_number']


class ResetPasswordTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordToken
        fields = ['user', 'token', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'username', 'address', 'phone_number', 'item_name', 'quantity', 'price']


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderHistory
        fields = ['order', 'item_name', 'quantity']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['order', 'payment_amount', 'payment_date']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'phone_number']
