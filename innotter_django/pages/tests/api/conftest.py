import pytest
from faker import Faker
from pytest_factoryboy import register
from pages.tests.api.factories import PageFactory


register(PageFactory, 'private_page', is_private=True)
register(PageFactory, 'not_private_page')


@pytest.fixture
def page_for_serializer(user):
    faker = Faker()
    return {
        'name': faker.name(),
        'uuid': faker.ean(),
        'description': faker.text(),
        'image': faker.image_url(),
        'owner': user.id,
        'is_private': False,
    }
