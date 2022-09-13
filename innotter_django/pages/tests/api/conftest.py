import pytest
import factory
from pytest_factoryboy import register
from django.urls import reverse
from rest_framework.test import APIClient
from pages.models import Page
from users.tests.api.conftest import UserFactory, access_token


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    name = factory.Faker('first_name')
    uuid = factory.Faker('ean')
    description = factory.Faker('text')
    image = factory.Faker('file_name')
    owner = factory.LazyAttribute(lambda x: UserFactory())
    is_private = False


register(PageFactory, 'private_page', is_private=True)
register(PageFactory, 'not_private_page')


@pytest.fixture
def page_for_serializer():
    return {
        'name': 'name',
        'uuid': '12345',
        'description': 'description',
        'image': 'image',
        'owner': 1,
        'is_private': True,
    }
