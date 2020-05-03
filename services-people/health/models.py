import uuid

from django.db import models

from people.models import Person


class Health(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    vulnerability_score = models.FloatField()
