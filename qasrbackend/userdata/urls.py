from django.urls import path
from .views import SignupView, LoginView, PasswordResetView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('passwordreset/', PasswordResetView.as_view(), name='password_reset'),
]
