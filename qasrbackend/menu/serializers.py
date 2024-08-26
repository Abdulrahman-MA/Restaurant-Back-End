from rest_framework import serializers
from .models import MenuItem, Category


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('name', 'image_path', 'description', 'price')


class ArMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ('ar_name', 'image_path', 'ar_description', 'price')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'image_path']


class ArCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['ar_name', 'image_path']


class CategoryItemSerializer(serializers.ModelSerializer):
    class Mete:
        model = MenuItem, Category
        fields = ('name', 'image_path', 'description', 'price', 'half_price', 'third_price', 'quart_price')


class ArCategoryItemSerializer(serializers.ModelSerializer):
    class Mete:
        model = MenuItem, Category
        fields = ('ar_name', 'image_path', 'ar_description', 'price', 'half_price', 'third_price', 'quart_price')
