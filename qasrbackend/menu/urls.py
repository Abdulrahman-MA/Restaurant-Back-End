from django.urls import path
from .views import menu_items, item_detail, categories

urlpatterns = [
    path('menu-items/', menu_items, name='menu-items-list'),
    path('menu-items/<str:name>/', item_detail, name='menu-item-detail'),
    path('categories/', categories, name='menu-item-detail'),

]
