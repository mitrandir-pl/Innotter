from rest_framework import viewsets, status, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from users.serializers import UserSerializer
from users.models import User
from users.auth import generate_refresh_token, generate_access_token


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        response = Response()
        if (email is None) or (password is None):
            raise exceptions.AuthenticationFailed(
                'email and password required')

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
