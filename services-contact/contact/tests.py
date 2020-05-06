import uuid

from django.test import TestCase
from django.urls import reverse

from .models import Contact, Person


class ContactViewTests(TestCase):
    def test_post_contact_creates_contact_and_person_objects(self):
        self.assertEqual(Contact.objects.count(), 0)
        self.assertEqual(Person.objects.count(), 0)

        person_id_0001 = uuid.uuid4()
        person_id_0002 = uuid.uuid4()

        people_ids = [person_id_0001, person_id_0002]
        people_ids = [str(pid) for pid in people_ids]

        response = self.client.post(
            reverse("contact:contact"),
            {"people_ids": people_ids},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Person.objects.filter(person_id=person_id_0001).count(), 1)
        self.assertEqual(Person.objects.filter(person_id=person_id_0002).count(), 1)

        contact = Contact.objects.get()
        self.assertEqual(
            set(str(pid) for pid in contact.people.values_list("person_id", flat=True)),
            set(people_ids),
        )

        self.assertEqual(response.json(), {"id": str(contact.pk)})

    def test_post_contact_creates_contact_and_adds_existing_person_objects(self):
        self.assertEqual(Contact.objects.count(), 0)

        person_id_0001 = uuid.uuid4()
        Person.objects.create(person_id=person_id_0001)
        person_id_0002 = uuid.uuid4()
        Person.objects.create(person_id=person_id_0002)

        people_ids = [person_id_0001, person_id_0002]
        people_ids = [str(pid) for pid in people_ids]

        response = self.client.post(
            reverse("contact:contact"),
            {"people_ids": people_ids},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Person.objects.filter(person_id=person_id_0001).count(), 1)
        self.assertEqual(Person.objects.filter(person_id=person_id_0002).count(), 1)

        contact = Contact.objects.get()
        self.assertEqual(
            set(str(pid) for pid in contact.people.values_list("person_id", flat=True)),
            set(people_ids),
        )
