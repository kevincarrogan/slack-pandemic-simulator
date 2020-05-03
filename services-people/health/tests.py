from unittest.mock import patch

from django.test import TestCase

from people.models import Person

from .models import Health


class HealthModelTests(TestCase):

    def test_health_model_created_on_person_creation(self):
        mock_vulnerability_score = .5

        with patch('health.signals.get_vulnerability_score') as mock_get_vulnerability_score:
            mock_get_vulnerability_score.return_value = mock_vulnerability_score
            person = Person.objects.create()

        health = Health.objects.get(person=person)

        self.assertEqual(health.person, person)
        self.assertEqual(health.vulnerability_score, mock_vulnerability_score)
