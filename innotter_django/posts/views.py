from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from posts.serializers import PostSerializer
from posts.models import Post
from posts.tasks import send_notifications
from pages.permissions import IsOwner
from rest_framework.response import Response
from users.permissions import IsAdmin, IsModerator
from users.serializers import UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_permissions(self):
        permissions = {
            'retrieve': [IsAuthenticated],
            'list': [IsAdmin | IsModerator],
            'create': [IsAuthenticated],
            'update': [IsOwner],
            'partial_update': [IsOwner],
            'destroy': [IsAdmin | IsModerator | IsOwner],
            'total_likes': [IsAuthenticated, IsOwner],
        }
        permissions_for_action = permissions.get(
            self.action, [IsAuthenticated]
        )
        return [permission() for permission in permissions_for_action]

    @action(detail=True, methods=['post'])
    def set_like(self, request, pk):
        post = Post.objects.get(pk=pk)
        if post.likes.filter(pk=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def total_likes(self, request, pk):
        post = Post.objects.get(pk=pk)
        total_likes = post.total_likes
        return Response({'total_likes': total_likes},
                        status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def like_user_list(self, request, pk):
        post = Post.objects.get(pk=pk)
        users_list = post.likes.all()
        users = UserSerializer(users_list, many=True)
        return Response(users.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def liked_posts(self, request):
        posts = request.user.likes.all()
        serialized_posts = PostSerializer(posts, many=True)
        return Response(serialized_posts.data,
                        status=status.HTTP_200_OK)
