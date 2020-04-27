import uuid

from django.db import models

from teams.models import Team


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    slack_id = models.CharField(max_length=255)
    person_id = models.UUIDField()
