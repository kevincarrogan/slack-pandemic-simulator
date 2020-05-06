from django.db import models

from messages.models import Message


class Contact(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    contact_id = models.UUIDField()
