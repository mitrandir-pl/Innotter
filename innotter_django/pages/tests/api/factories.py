import factory
from users.tests.api.factories import UserFactory
from pages.models import Page


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    name = factory.Faker('first_name')
    uuid = factory.Faker('ean')
    description = factory.Faker('text')
    image = factory.Faker('image_url')
    owner = factory.SubFactory(UserFactory)
    is_private = False

