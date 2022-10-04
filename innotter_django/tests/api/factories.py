import factory
from pages.models import Page
from users.models import User
from posts.models import Post


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('email')
    username = factory.Faker('first_name')
    title = factory.Faker('name')
    password = factory.PostGenerationMethodCall('set_password', 'password')
    role = 'user'
    is_blocked = False


class PageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Page

    name = factory.Faker('first_name')
    uuid = factory.Faker('ean')
    description = factory.Faker('text')
    image = factory.Faker('image_url')
    owner = factory.SubFactory(UserFactory)
    is_private = False


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post

    page = factory.SubFactory(PageFactory)
    content = factory.Faker('text')
    created_at = factory.Faker('past_datetime')
    updated_at = factory.Faker('date_time')
