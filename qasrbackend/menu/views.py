from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer
from rest_framework import status
from rest_framework.response import Response


@api_view(['GET'])
def menu_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return JsonResponse({'items_data': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse({'categories': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def item_detail(request, name, category):

    try:
        item = MenuItem.objects.get(name=name, category=category)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MenuItemSerializer(item)
        return JsonResponse({'item_info': serializer.data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
