from django.urls import path
from .views import menu_items, item_detail, categories, category_items

urlpatterns = [
    # Menu items API endpoints
    path('menu-items/', menu_items, name='menu-items-list'),
    path('menu-items/<str:name>/', item_detail, name='menu-item-detail'),

    # Category items API endpoints
    path('categories/', categories, name='menu-item-detail'),
    path('categories/<slug:category_name>/', category_items, name='category_menu_items'),
]
