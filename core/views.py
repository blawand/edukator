# core/views.py
from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Edukator!")

class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer