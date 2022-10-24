import boto3
from pages.models import Page
from core.settings import (EMAIL_ADDRESS, LOCAL_AWS_URL, AWS_ACCESS_KEY_ID,
                           AWS_SECRET_ACCESS_KEY, AWS_SES_REGION_NAME)


class EmailService:
    CHARSET = 'UTF-8'

    def __init__(self):
        self.ses = boto3.client('ses', endpoint_url=LOCAL_AWS_URL,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=AWS_SES_REGION_NAME)
        self.ses.verify_email_address(EmailAddress='Innotter@gmail.com')

    def send_notifications_about_new_post(self, page_id: int) -> None:
        destination = self.get_destination(page_id)
        message = self.get_message()
        self.ses.send_email(
            Destination=destination,
            Message=message,
            Source=EMAIL_ADDRESS
        )

    def get_message(self) -> dict[str: dict[str: dict[str: str]]]:
        return {
            'Body': {
                'Html': {
                    'Data': self.get_html_data(),
                    'Charset': self.CHARSET,
                },
            },
            'Subject': {
                'Data': 'New Post!!!',
                'Charset': self.CHARSET,
            }
        }

    def get_html_data(self) -> str:
        return f"""<html>
            <head></head>
            <h2>Check out your friend's new post</h2>
            <h1>New post!<h1>
            </body>
        </html>"""

    def get_destination(self, page_id: int) -> dict[str: list[str]]:
        page = Page.objects.get(pk=page_id)
        emails = page.followers.all().values_list('email', flat=True)
        return {'ToAddresses': [i for i in emails]}
