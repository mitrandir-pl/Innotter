from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='pages')
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='pages'
    )
    followers = models.ManyToManyField(
        User, related_name='follows'
    )
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        User, related_name='requests'
    )
    unblock_date = models.DateTimeField(null=True, blank=True)
