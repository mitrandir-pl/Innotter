import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from users.models import User
from core.error_messages import (NO_SUCH_USER_OR_USER_NOT_ACTIVE_MESSAGE,
                                 TOKEN_PREFIX_ERROR_MESSAGE,
                                 ACCESS_TOKEN_EXPIRED_MESSAGE,)


class JWTAuthentication(BaseAuthentication):

    def validate_authorization_header(self, authorization_header):
        try:
            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            user = User.objects.filter(email=payload['user_email']).first()
            if user is None or not user.is_active:
                raise exceptions.AuthenticationFailed(
                    NO_SUCH_USER_OR_USER_NOT_ACTIVE_MESSAGE
                )
        except IndexError:
            raise exceptions.AuthenticationFailed(TOKEN_PREFIX_ERROR_MESSAGE)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(ACCESS_TOKEN_EXPIRED_MESSAGE)

    def _get_access_token(self, authorization_header):
        access_token = authorization_header.split(' ')[1]
        return access_token

    def _get_payload(self, access_token):
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256']
        )
        return payload

    def _get_user(self, payload):
        user = User.objects.filter(email=payload['user_email']).first()
        return user

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        else:
            self.validate_authorization_header(authorization_header)
        access_token = self._get_access_token(authorization_header)
        payload = self._get_payload(access_token)
        user = self._get_user(payload)

        return user, None
