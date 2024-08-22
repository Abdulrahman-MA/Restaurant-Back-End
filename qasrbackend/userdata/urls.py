from django.urls import path
from .views import reset_password, signup, login, change_email, get_all_users

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('passwordreset/', reset_password, name='password_reset'),
    path('changeemail', change_email, name='change_email'),
    path('getusers/',get_all_users, name='get users')
]
