import pytest
import factory
from pytest_factoryboy import register
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('first_name')
    title = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    role = 'user'
    is_blocked = False


@pytest.fixture
def user_password():
    return 'password'


register(UserFactory)
register(UserFactory, 'admin', role='admin')


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_for_serializer():
    return {
        'username': 'username',
        'email': 'email@a.com',
        'role': 'user',
        'title': 'title',
        'password': 'password',
    }


@pytest.fixture
def refresh_token(client, user, user_password):
    response = login(client, user.email, user_password)
    return response.json()['refresh_token']


@pytest.fixture
def admin_access_token(client, admin, user_password):
    response = login(client, admin.email, user_password)
    return response.json()['access_token']


def login(client, email, password):
    url = reverse('users-login')
    data = {'user': {
        'email': email,
        'password': password,
    }}
    return client.post(url, data, format='json')
