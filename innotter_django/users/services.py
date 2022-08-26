import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework import exceptions
from users.models import User
from users.serializers import UserLoginSerializer, UserSerializer
from users.auth import generate_refresh_token, generate_access_token


class LoginService:
    def __init__(self, request):
        self.user = request.data.get('user', {})

    def validate(self):
        serialized_user = UserLoginSerializer(data=self.user)
        serialized_user.is_valid(raise_exception=True)
        # email_error = serialized_user.errors.get('email')[0]
        # if email_error.code == 'unique':
        #     pass
        # else:
        #     serialized_user.is_valid(raise_exception=True)

    def get_user(self):
        email = self.user.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        return user

    def get_response(self):
        user = self.get_user()
        response = Response()
        response.set_cookie(
            key='refreshtoken',
            value=generate_refresh_token(user),
            httponly=True
        )
        response.data = {
            'access_token': generate_access_token(user),
            'user': UserSerializer(user).data,
        }
        return response


class RefreshTokenService:
    def __init__(self, request):
        self.__token = request.COOKIES.get('refreshtoken')
        if self.__token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.'
            )

    @property
    def token(self):
        return self.__token


class PayLoadService:
    def __init__(self, refresh_token):
        try:
            self.__payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.'
            )

    def get_user(self):
        user = User.objects.filter(id=self.__payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
        return user
