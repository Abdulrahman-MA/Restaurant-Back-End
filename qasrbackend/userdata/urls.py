from django.urls import path
from .views import reset_password, signup, login

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('passwordreset/', reset_password, name='password_reset'),
]
