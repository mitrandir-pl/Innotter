import pytest
from datetime import datetime, timedelta
from faker import Faker
from pytest_factoryboy import register
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.test import APIClient
from tests.api.factories import PageFactory, UserFactory, PostFactory

register(UserFactory)
register(UserFactory, 'admin', role='admin')
register(PageFactory, 'private_page', is_private=True)
register(PageFactory, 'not_private_page')
register(PageFactory)
register(PostFactory)


@pytest.fixture
def user_password() -> str:
    return 'password'


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_for_serializer() -> dict[str: str]:
    faker = Faker()
    return {
        'username': faker.first_name(),
        'email': faker.email(),
        'role': 'user',
        'title': faker.name(),
        'password': faker.password(),
    }


@pytest.fixture
def refresh_token(client, user: UserFactory, user_password: str) -> str:
    response = login(client, user.email, user_password)
    return response.json()['refresh_token']


@pytest.fixture
def admin_access_token(client, admin: UserFactory, user_password: str) -> str:
    response = login(client, admin.email, user_password)
    return response.json()['access_token']


@pytest.fixture
def access_token(client, user: UserFactory, user_password: str) -> str:
    response = login(client, user.email, user_password)
    return response.json()['access_token']


def login(client, email: str, password: str) -> Response:
    url = reverse('users-login')
    data = {'user': {
        'email': email,
        'password': password,
    }}
    return client.post(url, data, format='json')


@pytest.fixture
def page_for_serializer(user: UserFactory) -> dict[str: str]:
    faker = Faker()
    return {
        'name': faker.name(),
        'uuid': faker.ean(),
        'description': faker.text(),
        'image': faker.image_url(),
        'owner': user.id,
        'is_private': False,
    }


@pytest.fixture
def post_for_serializer(user: UserFactory, not_private_page: PageFactory) -> dict[str: str]:
    faker = Faker()
    return {
        'page': not_private_page.id,
        'content': faker.text(),
        'created_at': faker.past_datetime,
        'updated_at': faker.date_time,
    }


@pytest.fixture
def unblock_date() -> dict[str: str]:
    unblock_date = datetime.now() + timedelta(days=1)
    unblock_date = str(unblock_date.replace(microsecond=0))
    return {'unblock_date': unblock_date}
