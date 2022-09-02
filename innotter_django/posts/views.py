from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from posts.serializers import PostSerializer
from posts.models import Post
from posts.permissions import IsAdmin, IsModerator, IsOwner


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        permissions = {
            'retrieve': [IsAuthenticated],
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
