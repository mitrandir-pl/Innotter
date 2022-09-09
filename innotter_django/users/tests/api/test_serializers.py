import pytest
from users.serializers import UserSerializer
from users.models import User


class TestUserSerializer:

    @pytest.mark.django_db
    def test_create_user(self, user_for_serializer):
        serializer = UserSerializer(data=user_for_serializer)
        if serializer.is_valid():
            serializer.save()
        assert User.objects.filter(email=user_for_serializer['email']).first()

    @pytest.mark.django_db
    def test_update_user(self, user, user_for_serializer):
        new_email = 'new_email@a.com'
        user_for_serializer['email'] = new_email
        serializer = UserSerializer(instance=user,
                                    data=user_for_serializer)
        if serializer.is_valid():
            serializer.save()
        assert User.objects.filter(email=new_email).first()
