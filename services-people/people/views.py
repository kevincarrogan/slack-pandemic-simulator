from django.http import JsonResponse
from django.views import View

from .models import Person


class PersonView(View):
    def post(self, request):
        person = Person.objects.create()

        return JsonResponse({"id": person.pk})
