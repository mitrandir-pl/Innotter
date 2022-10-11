import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestPostAPI:

    def test_create(self, client, access_token, post_for_serializer):
        url = reverse('posts-list')
        response = client.post(url, post_for_serializer,
                               HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.status_code == status.HTTP_201_CREATED

    def test_set_like(self, client, user, post, access_token):
        client.post(reverse('posts-set-like', kwargs={'pk': 1}),
                    HTTP_AUTHORIZATION=f'token {access_token}')
        assert post.likes.first() == user
        client.post(reverse('posts-set-like', kwargs={'pk': 1}),
                    HTTP_AUTHORIZATION=f'token {access_token}')
        assert post.likes.first() is None

    def test_like_user_list(self, client, post, user, access_token):
        client.post(reverse('posts-set-like', kwargs={'pk': 1}),
                    HTTP_AUTHORIZATION=f'token {access_token}')
        response = client.get(reverse('posts-like-user-list', kwargs={'pk': 1}),
                              HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.status_code == status.HTTP_200_OK
        assert type(response.json()) is list
        assert response.json()[0].get('id') == user.pk

    def test_total_likes(self, client, post, user, access_token):
        url = reverse('posts-total-likes', kwargs={'pk': 1})
        response = client.get(url, HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.data.get('total_likes') == 0
        client.post(reverse('posts-set-like', kwargs={'pk': 1}),
                    HTTP_AUTHORIZATION=f'token {access_token}')
        response = client.get(url, HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.data.get('total_likes') == 1

    def test_liked_posts(self, client, post, access_token):
        client.post(reverse('posts-set-like', kwargs={'pk': 1}),
                    HTTP_AUTHORIZATION=f'token {access_token}')
        url = reverse('posts-liked-posts')
        response = client.get(url, HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.json()[0].get('id') == post.pk
