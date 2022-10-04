from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from pages.serializers import PageSerializer, PageSimpleSerializer, TagSerializer
from pages.models import Page, Tag
from pages.permissions import IsOwner, IsNotPrivate
from users.permissions import IsAdmin, IsModerator
from users.services import AdminService
from pages.services import PageService


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()

    def get_serializer_class(self):
        serializer_classes = {
            'create': PageSimpleSerializer,
        }
        serializer_class_for_action = serializer_classes.get(
            self.action, PageSerializer
        )
        return serializer_class_for_action

    def get_permissions(self):
        permissions = {
            'retrieve': [IsAuthenticated, IsNotPrivate | IsAdmin | IsModerator | IsOwner],
            'update': [IsAuthenticated, IsOwner],
            'partial_update': [IsAuthenticated, IsOwner],
            'destroy': [IsAuthenticated, IsAdmin | IsModerator | IsOwner],
            'block_page': [IsAuthenticated, IsAdmin | IsModerator],
            'allow_current_follow_request': [IsAuthenticated, IsOwner],
            'allow_all_follow_request': [IsAuthenticated, IsOwner],
        }
        permissions_for_action = permissions.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permissions_for_action]

    @action(detail=True, methods=['post'])
    def block_page(self, request, pk):
        admin_service = AdminService()
        blocked_page = admin_service.block_page(request.data, pk)
        if blocked_page:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def subscribe(self, request, pk):
        page_service = PageService()
        page_service.subscribe(request.user, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def follow_requests(self, request, pk):
        page_service = PageService()
        follow_requests = page_service.get_follow_requests(pk)
        if follow_requests:
            return Response(follow_requests.data,
                            status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def allow_current_follow_request(self, request, pk):
        page_service = PageService()
        page_service.allow_current_follow_request(request.data, pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def allow_all_follow_request(self, request, pk):
        page_service = PageService()
        page_service.allow_all_follow_request(pk)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_tag(self, request, pk):
        serialized_tag = TagSerializer(data=request.data)
        if serialized_tag.is_valid(raise_exception=True):
            tag = serialized_tag.save()
            page = Page.objects.get(pk=pk)
            page.tags.add(tag)
            return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
