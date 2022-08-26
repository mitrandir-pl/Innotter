from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.models import User
from users.permissions import IsAdmin, IsModerator, IsOwner
from users.auth import generate_access_token
from users.services import LoginService, RefreshTokenService, PayLoadService


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
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
        login_service = LoginService(request)
        login_service.validate()
        response = login_service.get_response()
        return response

    @action(detail=False, methods=['post'])
    def refresh_token(self, request):
        refresh_token_service = RefreshTokenService(request)
        payload_service = PayLoadService(refresh_token_service.token)
        user = payload_service.get_user()
        access_token = generate_access_token(user)
        return Response({'access_token': access_token})
