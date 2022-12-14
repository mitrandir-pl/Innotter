import pytest
from rest_framework import status
from django.urls import reverse


@pytest.mark.django_db
class TestUserAPI:

    def test_successful_login(self, client, user, user_password):
        url = reverse('users-login')
        data = {'user': {
            'email': user.email,
            'password': user_password,
        }}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['refresh_token'] and \
               response.data['access_token']

    def test_unsuccessful_login(self, client):
        url = reverse('users-login')
        data = {'user': {
            'email': 'wrong_email@a.com',
            'password': 'wrong password',
        }}
        response = client.post(url, data, format="json")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_refresh_token(self, client, refresh_token):
        url = reverse('users-refresh-token')
        data = {'refresh_token': refresh_token}
        response = client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['access_token']

    def test_block_user(self, client, admin, admin_access_token):
        blocked_user_url = reverse('users-detail', kwargs={'pk': admin.id})
        user_before_block = client.get(blocked_user_url)
        url = reverse('users-block-user', kwargs={'pk': admin.id})
        response = client.post(
            url, HTTP_AUTHORIZATION=f'token {admin_access_token}'
        )
        user_after_block = client.get(blocked_user_url)
        assert response.status_code == status.HTTP_200_OK
        assert user_before_block.data['is_blocked'] is False
        assert user_after_block.data['is_blocked'] is True
