from rest_framework import viewsets
from posts.serializers import PostSerializer
from posts.models import Post


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
