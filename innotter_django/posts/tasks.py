from celery import shared_task
from posts.services import EmailService


@shared_task
def send_notifications(post_creator_name: str, page_id: int, post_link: str):
    email_service = EmailService()
    email_service.send_notifications_about_new_post(
        post_creator_name, page_id, post_link
    )
