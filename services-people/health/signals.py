import random

from django.db.models.signals import post_save
from django.dispatch import receiver

from people.models import Person

from .models import Health


def get_vulnerability_score():
    return random.randint(0, 10) / 10


@receiver(post_save, sender=Person)
def create_health_model(sender, instance, created, **kwargs):
    if not created:
        return

    Health.objects.create(
        person=instance,
        vulnerability_score=get_vulnerability_score(),
    )
