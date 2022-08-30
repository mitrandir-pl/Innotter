import jwt
from django.conf import settings
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import UserSerializer, UserLoginSerializer
from users.models import User
from users.permissions import IsAdmin, IsModerator, IsOwner
from users.auth import generate_access_token, generate_refresh_token


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
        user = User.objects.filter(
            id=self.__payload.get('user_id')
        ).first()
        if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User not found or not active'
            )
        return user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permissions = {
            'update': [IsAdmin | IsModerator | IsOwner],
            'partial_update': [IsAdmin | IsModerator | IsOwner],
            'destroy': [IsAdmin | IsModerator | IsOwner],
        }
        permissions_for_action = permissions.get(
            self.action, [AllowAny]
        )
        return [permission() for permission in permissions_for_action]

    @action(detail=False, methods=['post'])
    def login(self, request):
        user_data = request.data.get('user', {})
        serialized_user = UserLoginSerializer(data=user_data)
        serialized_user.is_valid(raise_exception=True)
        email = user_data.get('email')
        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
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

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        refresh_token_service = RefreshTokenService(request)
        payload_service = PayLoadService(refresh_token_service.token)
        user = payload_service.get_user()
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})
