import json

from django.http import HttpResponse
from django.views import View


class MemberView(View):
    def post(self, request):
        event = json.loads(request.body)

        return HttpResponse("OK")
