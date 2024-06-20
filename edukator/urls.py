# edukator/urls.py
from django.contrib import admin
from django.urls import path, include
from core.views import UserCreateView, home, LogoutView, GetCSRFToken, FileUploadView, SlideListCreateView, SlideDetailView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', UserCreateView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='api_login'),
    path('api/logout/', LogoutView.as_view(), name='api_logout'),
    path('api/csrf/', GetCSRFToken.as_view(), name='get_csrf_token'),
    path('', home, name='home'),
    path('api/', include('rest_framework.urls')),
    path('api/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/slides/', SlideListCreateView.as_view(), name='slide-list-create'),
    path('api/slides/<int:pk>/', SlideDetailView.as_view(), name='slide-detail'),
]