import pytest
from rest_framework import status
from django.urls import reverse


class TestUserAPI:

    @pytest.mark.django_db
    def test_successful_login(self, client, user):
        url = reverse('users-login')
        data = {'user': {
            'email': user.email,
            'password': '123',
        }}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['refresh_token'] and \
               response.data['access_token']

    @pytest.mark.django_db
    def test_unsuccessful_login(self, client):
        url = reverse('users-login')
        data = {'user': {
            'email': 'wrong_email@a.com',
            'password': 'wrong password',
        }}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_refresh_token(self, client, refresh_token):
        url = reverse('users-refresh-token')
        data = {'refresh_token': refresh_token}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['access_token']

    @pytest.mark.django_db
    def test_block_user(self, client, admin_access_token):
        blocked_user_url = reverse('users-detail', kwargs={'pk': 1})
        user_before_block = client.get(blocked_user_url)
        url = reverse('users-block-user', kwargs={'pk': 1})
        response = client.post(
            url, HTTP_AUTHORIZATION=f'token {admin_access_token}'
        )
        user_after_block = client.get(blocked_user_url)
        assert response.status_code == status.HTTP_200_OK
        assert user_before_block.data['is_blocked'] is False
        assert user_after_block.data['is_blocked'] is True
