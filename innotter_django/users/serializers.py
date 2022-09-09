from rest_framework import serializers, exceptions
from users.auth import generate_refresh_token, generate_access_token
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'image_s3_path',
            'role', 'title', 'is_blocked', 'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'email', 'password',
            'refresh_token', 'access_token',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None or not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User not found or not active'
            )
        if user.check_password(data['password']):
            data['refresh_token'] = generate_refresh_token(data)
            data['access_token'] = generate_access_token(data)
            return data
        else:
            raise exceptions.AuthenticationFailed(
                'Wrong password'
            )
