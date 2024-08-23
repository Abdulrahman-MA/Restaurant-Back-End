from rest_framework import serializers
from .models import MenuItem, Category


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('name', 'image_path', 'description', 'price')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'image_path']


class CategoryItemSerializer(serializers.ModelSerializer):
    class Mete:
        model = MenuItem, Category
        fields = ('name', 'image_path', 'description', 'price', 'half_price', 'third_price', 'quart_price')
