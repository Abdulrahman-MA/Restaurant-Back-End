from django.urls import path
from .views import menu_items, item_detail, categories, category_items, ar_category_items, ar_categories, ar_item_detail

urlpatterns = [
    # Menu items API endpoints
    path('menu-items/', menu_items, name='menu-items-list'),
    path('menu-items/<str:name>/', item_detail, name='menu-item-detail'),
    path('menu-items/<str:name>/ar/', ar_item_detail, name='menu-item-detail'),


    # Category items API endpoints
    path('categories/', categories, name='menu-item-detail'),
    path('categories/ar/', ar_categories, name='menu-item-detail'),
    path('categories/<slug:category_name>/', category_items, name='category_menu_items'),
    path('categories/<slug:category_name>/ar/', ar_category_items, name='category_menu_items'),
]
