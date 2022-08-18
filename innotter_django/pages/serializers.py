from rest_framework import serializers
from pages.models import Page, Tag


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            'id', 'name', 'uuid', 'description', 'owner',
            'image', 'is_private', 'unblock_date',
        )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')
