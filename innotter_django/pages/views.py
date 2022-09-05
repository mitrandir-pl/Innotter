from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from pages.serializers import PageSerializer, TagSerializer
from pages.models import Page, Tag
from pages.permissions import IsOwner, IsNotPrivate
from users.permissions import IsAdmin, IsModerator


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()

    def get_permissions(self):
        permissions = {
            'retrieve': [IsNotPrivate | IsAdmin | IsModerator | IsOwner],
            'list': [IsAdmin, IsModerator],
            'create': [IsAuthenticated],
            'update': [IsOwner],
            'partial_update': [IsOwner],
            'destroy': [IsAdmin | IsModerator | IsOwner],
        }
        permissions_for_action = permissions.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permissions_for_action]


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
