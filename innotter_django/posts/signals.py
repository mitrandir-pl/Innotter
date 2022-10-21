from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
from posts.tasks import send_notifications


@receiver(post_save, sender=Post)
def create_user_profile(sender, instance, created, **kwargs):
    page_id = instance.page.id
    send_notifications.delay(page_id)
