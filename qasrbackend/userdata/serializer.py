from django.contrib.auth import get_user_model
from .models import Users
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number')
        )
        return user


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        Users = get_user_model()
        if not Users.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email address not found")
        return email
