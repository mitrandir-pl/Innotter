import pytest
from django.urls import reverse
from posts.services import EmailService
from users.models import User


@pytest.mark.django_db
class TestEmailService:

    email_service = EmailService()

    def test_get_message(self):
        message = self.email_service.get_message()
        assert isinstance(message, dict)
        assert message.get('Body')
        assert message.get('Subject')

    def test_html_data(self):
        html_data = self.email_service.get_html_data()
        assert isinstance(html_data, str)

    def test_destination(self, client, user, not_private_page, access_token):
        url = reverse('pages-subscribe', kwargs={'pk': not_private_page.id})
        client.post(url, HTTP_AUTHORIZATION=f'token {access_token}')
        page = client.get(reverse('pages-detail', kwargs={'pk': not_private_page.id}),
                          HTTP_AUTHORIZATION=f'token {access_token}')
        follower = page.data.get('followers', [])[0]

        destination = self.email_service.get_destination(not_private_page.pk)
        follower_email = destination.get('ToAddresses')[0]
        follower_ = User.objects.filter(email=follower_email).first()
        assert follower_.pk == follower
