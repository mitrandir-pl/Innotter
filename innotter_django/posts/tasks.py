from celery import shared_task
from posts.services import EmailService


@shared_task
def send_notifications(page_id: int) -> None:
    email_service = EmailService()
    email_service.send_notifications_about_new_post(page_id)
