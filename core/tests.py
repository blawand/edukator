# core/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import Slide

class SlideModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_slide_creation(self):
        slide = Slide.objects.create(user=self.user, title="Test Slide", content="This is a test slide.")
        self.assertEqual(slide.title, "Test Slide")
        self.assertEqual(slide.content, "This is a test slide.")
        self.assertEqual(slide.user, self.user)

class SlideAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_slide(self):
        data = {
            'title': 'Test Slide',
            'content': 'This is a test slide.'
        }
        response = self.client.post('/api/slides/', data)
        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Slide')
        self.assertEqual(response.data['content'], 'This is a test slide.')

    def test_get_slides(self):
        Slide.objects.create(user=self.user, title='Test Slide 1', content='This is the first test slide.')
        Slide.objects.create(user=self.user, title='Test Slide 2', content='This is the second test slide.')
        response = self.client.get('/api/slides/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)