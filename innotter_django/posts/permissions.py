from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.role == 'admin'
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.user and
            request.user.role == 'moderator'
        )


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
