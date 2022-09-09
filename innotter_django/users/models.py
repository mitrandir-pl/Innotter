from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, username,
                         password, **other_fields):

        for field in ('is_staff', 'is_superuser', 'is_active'):
            other_fields.setdefault(field, True)

        permissions = ('is_staff', 'is_superuser')
        for permission in permissions:
            if other_fields.get(permission) is not True:
                raise ValueError(
                    f'Superuser must be assigned to {permission}=True.'
                )

        return self.create_user(email, username,
                                password, **other_fields)

    def create_user(self, email, username,
                    password, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          username=username,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    objects = CustomUserManager()

    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(max_length=200, null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
