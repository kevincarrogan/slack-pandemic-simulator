import json

from django.http import JsonResponse
from django.views import View

from .models import Contact, Person


class ContactView(View):
    def post(self, request):
        body = json.loads(request.body)

        contact = Contact.objects.create()
        for person_id in body["people_ids"]:
            person, _ = Person.objects.get_or_create(person_id=person_id)
            contact.people.add(person)

        return JsonResponse({"id": contact.pk})
