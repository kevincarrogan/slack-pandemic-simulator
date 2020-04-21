import uuid

from django.db import models


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team_id = models.CharField(max_length=255)
    bot_user_id = models.CharField(max_length=255)
    bot_access_token = models.CharField(max_length=255)

    def __str__(self):
        return self.team_id
