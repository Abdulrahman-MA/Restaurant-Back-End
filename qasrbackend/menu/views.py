from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import MenuItem
from .serializers import MenuItemSerializer


@api_view('GET')
def menu_items(request):
    if request.method == 'GET':
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
