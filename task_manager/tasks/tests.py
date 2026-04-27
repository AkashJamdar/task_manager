from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from.models import Task

# Create your tests here.
class TaskAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='akash', password='akash@1212')
        self.task = Task.objects.create(title='Task 1', description='Task 2', status='OPEN', user=self.user)
        self.client.force_authenticate(user=self.user)

    def test_jwt_login(self):
        url = reverse('token_obtain_pair')
        data = {'username': 'akash', 'password': 'akash@1212'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_get_task_authenticated(self):
        self.client.login(username='akash', password='akash@1212')
        url = reverse('task-detail', kwargs={'pk': self.task.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_task(self):
        self.client.login(username='akash', password='akash@1212')
        url = reverse('task-list')
        data = {'title': 'Task 1', 'description': 'Task 2', 'status': 'OPEN'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_list_without_authenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse('task-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)