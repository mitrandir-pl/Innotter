from enum import Enum
from rest_framework import permissions


class Role(Enum):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == Role.ADMIN.value
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.role == Role.ADMIN.value
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.role == Role.MODERATOR.value
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.role == Role.MODERATOR.value
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return obj == request.user
