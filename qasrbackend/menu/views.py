from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from .models import MenuItem, Category
from .serializers import MenuItemSerializer, CategorySerializer, ArMenuItemSerializer, ArCategorySerializer
from rest_framework import status


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve the items in a specific category.",
    responses={200: MenuItemSerializer(many=True)}
)
@api_view(['GET'])
def category_items(request, category_name):
    category = Category.objects.get(name=category_name)
    menu_items = MenuItem.objects.filter(category=category)
    serializer = MenuItemSerializer(menu_items, many=True)

    return JsonResponse({'menu_items': serializer.data})


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve the items in a specific category.",
    responses={200: MenuItemSerializer(many=True)}
)
@api_view(['GET'])
def ar_category_items(request, category_name):
    category = Category.objects.get(name=category_name)
    menu_items = MenuItem.objects.filter(category=category)
    serializer = ArMenuItemSerializer(menu_items, many=True)

    return JsonResponse({'menu_items': serializer.data})


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve all menu items.",
    responses={200: MenuItemSerializer(many=True)}
)
@api_view(['GET'])
def menu_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return JsonResponse({'items_data': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve all the categories in the menu.",
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET'])
def categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse({'categories': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve all the categories in the menu.",
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET'])
def ar_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = ArCategorySerializer(categories, many=True)
        return JsonResponse({'categories': serializer.data}, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve details of a specific menu item.",
    responses={200: MenuItemSerializer()}
)
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


@swagger_auto_schema(
    method='GET',
    operation_description="Retrieve details of a specific menu item.",
    responses={200: MenuItemSerializer()}
)
@api_view(['GET'])
def ar_item_detail(request, name, category):

    try:
        item = MenuItem.objects.get(name=name, category=category)
    except MenuItem.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ArMenuItemSerializer(item)
        return JsonResponse({'item_info': serializer.data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
