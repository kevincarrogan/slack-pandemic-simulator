import datetime
import uuid

from django.db import models

from channels.models import Channel
from members.models import Member


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    slack_timestamp = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def save(self, *args, **kwargs):
        timestamp, _ = self.slack_timestamp.split(".")
        timestamp = int(timestamp)
        timestamp = datetime.datetime.fromtimestamp(timestamp)
        self.timestamp = timestamp

        return super().save(*args, **kwargs)
