import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestPageAPI:

    def test_page_creation(self, client, access_token, page_for_serializer):
        url = reverse('pages-list')
        response = client.post(url, page_for_serializer,
                               HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.status_code == status.HTTP_201_CREATED

    def test_block_page(self, client, not_private_page, admin_access_token, unblock_date):
        url = reverse('pages-block-page', kwargs={'pk': 1})
        response = client.post(url, unblock_date,
                               HTTP_AUTHORIZATION=f'token {admin_access_token}')
        assert response.status_code == status.HTTP_200_OK

    def test_subscribe_on_not_private_page(self, client, not_private_page, user, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        page = client.get(reverse('pages-detail', kwargs={'pk': 1}),
                          HTTP_AUTHORIZATION=f'token {access_token}')
        followers = page.data.get('followers', [])
        assert user.pk in followers

    def test_subscribe_on_private_page(self, client, private_page, user, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        page = client.get(reverse('pages-detail', kwargs={'pk': 1}),
                          HTTP_AUTHORIZATION=f'token {access_token}')
        follow_requests = page.data.get('follow_requests', [])
        assert user.pk in follow_requests

    def test_follow_requests(self, client, private_page, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        url = reverse('pages-follow-requests', kwargs={'pk': 1})
        response = client.get(url, HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.status_code == status.HTTP_200_OK
        assert type(response.json()) is list

    def test_allow_current_follow_requests(self, client, user, private_page, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        url = reverse('pages-allow-current-follow-request', kwargs={'pk': 1})
        client.post(url, {'allow_following': user.pk},
                    HTTP_AUTHORIZATION=f'token {access_token}')
        page = client.get(reverse('pages-detail', kwargs={'pk': 1}),
                          HTTP_AUTHORIZATION=f'token {access_token}')
        follow_requests = page.data.get('follow_requests', [])
        followers = page.data.get('followers', [])
        assert user.pk not in follow_requests
        assert user.pk in followers

    def test_allow_all_follow_requests(self, client, user, private_page, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        url = reverse('pages-allow-all-follow-request', kwargs={'pk': 1})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        page = client.get(reverse('pages-detail', kwargs={'pk': 1}),
                          HTTP_AUTHORIZATION=f'token {access_token}')
        follow_requests = page.data.get('follow_requests', [])
        followers = page.data.get('followers', [])
        assert user.pk not in follow_requests
        assert user.pk in followers

    def test_add_tag(self, client, not_private_page, access_token):
        url = reverse('pages-add-tag', kwargs={'pk': 1})
        tag = {'name': 'new_tag'}
        response = client.post(url, tag, HTTP_AUTHORIZATION=f'token {access_token}')
        assert response.status_code == status.HTTP_200_OK
