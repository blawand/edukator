from django.contrib import admin
from django.urls import path, include
from core.views import UserCreateView, home
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urls import urlpatterns as rest_framework_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('', home, name='home'),
    path('api/', include('rest_framework.urls')),
]

# Add the logout route from rest_framework.urls
urlpatterns += [
    path('api/logout/', rest_framework_urls[0].callback, name='api_logout'),
]