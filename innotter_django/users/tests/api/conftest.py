from dataclasses import dataclass
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User


@dataclass
class TestUser:
    username: str = 'test_user'
    email: str = 'a@a.com'
    role: str = 'user'
    title: str = 'test'
    password: str = '123'


@dataclass
class TestAdmin:
    username: str = 'test_admin'
    email: str = 'admin@a.com'
    role: str = 'admin'
    title: str = 'test'
    password: str = '123'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    user = TestUser()
    return User.objects.create_user(
        username=user.username,
        email=user.email,
        role=user.role,
        title=user.title,
        password=user.password,
    )


@pytest.fixture
def admin():
    admin = TestAdmin()
    return User.objects.create_superuser(
        username=admin.username,
        email=admin.email,
        role=admin.role,
        title=admin.title,
        password=admin.password,
    )


@pytest.fixture
def user_for_serializer():
    user = TestUser()
    return {
        'username': user.username,
        'email': user.email,
        'role': user.role,
        'title': user.title,
        'password': user.password,
    }


@pytest.fixture
def refresh_token(client, user):
    user = TestUser()
    url = reverse('users-login')
    data = {'user': {
        'email': user.email,
        'password': user.password,
    }}
    response = client.post(url, data, format='json')
    return response.json()['refresh_token']


@pytest.fixture
def admin_access_token(client, admin):
    admin = TestAdmin()
    url = reverse('users-login')
    data = {'user': {
        'email': admin.email,
        'password': admin.password,
    }}
    response = client.post(url, data, format='json')
    return response.json()['access_token']
