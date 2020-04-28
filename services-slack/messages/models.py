import uuid

from django.db import models

from channels.models import Channel
from members.models import Member


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    slack_timestamp = models.CharField(max_length=255)
