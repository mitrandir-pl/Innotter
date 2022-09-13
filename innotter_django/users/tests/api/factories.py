import factory
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
