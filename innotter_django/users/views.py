import jwt
from django.conf import settings
from rest_framework import viewsets, exceptions
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.models import User
from users.auth import generate_refresh_token, generate_access_token
from users.permissions import IsAdmin, IsModerator, IsOwner


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        permissions = {
            'create': [AllowAny],
            'list': [AllowAny],
            'retrieve': [AllowAny],
            'login': [AllowAny],
            'refresh_token': [AllowAny],
        }
        permissions_for_action = permissions.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permissions_for_action]

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required'
            )

        user = User.objects.filter(email=email).first()
        if user is None:
            raise exceptions.AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('wrong password')

        serialized_user = UserSerializer(user).data

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
        response.data = {
            'access_token': access_token,
            'user': serialized_user,
        }

        return response

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.'
            )
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.'
            )
        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})
