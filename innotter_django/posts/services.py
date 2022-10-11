import boto3
from pages.models import Page


class EmailService:

    ENDPOINT_URL = 'http://localhost:4566/'
    EMAIL_SENDER = 'Innotter@gmail.com'
    CHARSET = 'UTF-8'

    def send_notifications_about_new_post(self, post_creator_name: str,
                                          page_id: int, post_link: str):
        ses = boto3.client('ses', endpoint_url=self.ENDPOINT_URL)
        destination = self.get_destination(page_id)
        message = self.get_message(post_creator_name, post_link)
        ses.send_email(
            Destination=destination,
            Message=message,
            Source=self.EMAIL_SENDER
        )

    def get_message(self, post_creator_name: str, post_link: str):
        return {
                    'Body': {
                        'Html': {
                            'Data': self.get_html_data(post_creator_name, post_link),
                            'Charset': self.CHARSET,
                        },
                    },
                    'Subject': {
                        'Data': 'New Post!!!',
                        'Charset': self.CHARSET,
                    }
        }

    def get_html_data(self, post_creator_name: str, post_link: str):
        return f"""<html>
            <head></head>
            <h2>Check out {post_creator_name} new post</h2>
            <a href="{post_link}">New post!</a>
            </body>
        </html>"""

    def get_destination(self, page_id: int):
        page = Page.objects.get(pk=page_id)
        emails = page.followers.all().values_list('email', flat=True)
        return {'ToAddresses': [i for i in emails]}
