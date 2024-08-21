from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('social/', include('rest_framework_social_oauth2.urls')),
    path('api/', include('userdata.urls')),
    path('api/', include('menu.urls')),
]
