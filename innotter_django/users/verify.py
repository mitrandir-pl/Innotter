import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from users.models import User


class JWTAuthentication(BaseAuthentication):

    def _get_access_token(self, authorization_header):
        try:
            access_token = authorization_header.split(' ')[1]
            return access_token
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

    def _get_payload(self, access_token):
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')

    def _get_user(self, payload):
        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
        return user

    def authenticate(self, request):

        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        access_token = self._get_access_token(authorization_header)
        payload = self._get_payload(access_token)
        user = self._get_user(payload)

        return user, None
