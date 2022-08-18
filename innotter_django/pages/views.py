from rest_framework import viewsets
from pages.serializers import PageSerializer, TagSerializer
from pages.models import Page, Tag


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
