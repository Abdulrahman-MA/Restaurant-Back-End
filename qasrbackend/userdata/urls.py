from django.urls import path
from .views import reset_password, signup, login, change_email

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('passwordreset/', reset_password, name='password_reset'),
    path('changeemail', change_email, name='change_email')
]
