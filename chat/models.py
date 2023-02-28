from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import models
from djrichtextfield.models import RichTextField


class Thread(models.Model):
    participants = models.ManyToManyField(get_user_model(), related_name="threads")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Message(models.Model):
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="sent_message"
    )
    text = RichTextField()
    thread = models.ForeignKey(
        Thread,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
