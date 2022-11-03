import jwt
from django.conf import settings
from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.serializers import UserSerializer, UserLoginSerializer
from users.models import User
from users.permissions import IsAdmin, IsModerator, IsOwner
from users.auth import generate_access_token, generate_refresh_token
from users.services import AdminService
from core.error_messages import (AUTHENTICATION_FAILED_MESSAGE,
                                 REFRESH_TOKEN_EXPIRED_MESSAGE)


class RefreshTokenService:
    def __init__(self, request):
        self.__token = request.data.get('refresh_token')
        if self.__token is None:
            raise exceptions.AuthenticationFailed(
                AUTHENTICATION_FAILED_MESSAGE
            )

    def validate_token(self):
        try:
            self.__payload = jwt.decode(
                self.__token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                REFRESH_TOKEN_EXPIRED_MESSAGE
            )

    def get_user(self):
        return {'email': self.__payload.get('user_email')}


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        permissions = {
            'update': [IsAuthenticated, IsAdmin | IsModerator | IsOwner],
            'partial_update': [IsAuthenticated, IsAdmin | IsModerator | IsOwner],
            'destroy': [IsAuthenticated, IsAdmin | IsModerator | IsOwner],
            'block_user': [IsAuthenticated, IsAdmin],
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
        return Response(serialized_user.data,
                        status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        refresh_token_service = RefreshTokenService(request)
        refresh_token_service.validate_token()
        user = refresh_token_service.get_user()
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})

    @action(detail=True, methods=['post'])
    def block_user(self, request, pk):
        admin_service = AdminService()
        admin_service.block_user(user_pk=pk)
        return Response(status=status.HTTP_200_OK)
