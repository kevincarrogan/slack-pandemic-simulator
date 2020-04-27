from django.test import TestCase
from django.urls import reverse

from .models import Person


class PersonViewTests(TestCase):
    def test_post_person(self):
        self.assertEqual(Person.objects.count(), 0)

        response = self.client.post(reverse("people:person"))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Person.objects.count(), 1)
        person = Person.objects.get()

        self.assertEqual(response.json(), {"id": str(person.pk)})
