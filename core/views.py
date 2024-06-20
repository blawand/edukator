# core/views.py
from django.http import HttpResponse
from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.middleware.csrf import get_token
from .models import UploadedFile, Slide
from .serializers import UserSerializer, UploadedFileSerializer, SlideSerializer
from .utils import create_presentation, add_slide

# Home view for simple response
def home(request):
    return HttpResponse("Welcome to Edukator!")

# User registration view
class UserCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Logout view
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# CSRF token view
class GetCSRFToken(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = get_token(request)
        return Response({'csrftoken': token})
    
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SlideListCreateView(generics.ListCreateAPIView):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreatePresentationView(APIView):
    def post(self, request):
        title = request.data.get('title')
        if not title:
            return Response({'error': 'Title is required'}, status=status.HTTP_400_BAD_REQUEST)
        presentation = create_presentation(title)
        return Response(presentation, status=status.HTTP_201_CREATED)

class AddSlideView(APIView):
    def post(self, request, presentation_id):
        slide_title = request.data.get('slide_title')
        slide_content = request.data.get('slide_content')
        if not slide_title or not slide_content:
            return Response({'error': 'Slide title and content are required'}, status=status.HTTP_400_BAD_REQUEST)
        response = add_slide(presentation_id, slide_title, slide_content)
        return Response(response, status=status.HTTP_201_CREATED)