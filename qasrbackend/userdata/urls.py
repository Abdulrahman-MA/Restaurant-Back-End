from django.urls import path
from .views import (
    user_list_create, user_detail, reset_password_token_list_create, reset_password_token_detail,
    order_list_create, order_detail, order_history_list_create, order_history_detail,
    payment_list_create, payment_detail, profile_list_create, profile_detail, login, signup
)

urlpatterns = [
    # User URLs
    path('users/allusers/', user_list_create, name='user-list-create'),
    path('users/<uuid:pk>/', user_detail, name='user-detail'),
    path('users/login', login, name='login'),
    path('users/signup', signup, name='signup'),


    # Reset Password Token URLs
    path('reset-tokens/', reset_password_token_list_create, name='reset-token-list-create'),
    path('reset-tokens/<int:pk>/', reset_password_token_detail, name='reset-token-detail'),

    # Order URLs
    path('orders/', order_list_create, name='order-list-create'),
    path('orders/<int:pk>/', order_detail, name='order-detail'),

    # Order History URLs
    path('order-history/', order_history_list_create, name='order-history-list-create'),
    path('order-history/<int:pk>/', order_history_detail, name='order-history-detail'),

    # Payment URLs
    path('payments/', payment_list_create, name='payment-list-create'),
    path('payments/<int:pk>/', payment_detail, name='payment-detail'),

    # Profile URLs
    path('profiles/', profile_list_create, name='profile-list-create'),
    path('profiles/<int:pk>/', profile_detail, name='profile-detail'),
]
