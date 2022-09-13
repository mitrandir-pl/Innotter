import pytest
from pytest_factoryboy import register
from django.urls import reverse
from rest_framework.test import APIClient
from users.tests.api.factories import UserFactory


register(UserFactory)
register(UserFactory, 'admin', role='admin')


@pytest.fixture
def user_password():
    return 'password'


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


@pytest.fixture
def access_token(client, user, user_password):
    response = login(client, user.email, user_password)
    return response.json()['access_token']


def login(client, email, password):
    url = reverse('users-login')
    data = {'user': {
        'email': email,
        'password': password,
    }}
    breakpoint()
    return client.post(url, data, format='json')
