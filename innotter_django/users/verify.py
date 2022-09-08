import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from users.models import User


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
                    'User not found or not active'
                )
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')

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
