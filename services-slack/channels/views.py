import json

from django.http import HttpResponse
from django.views import View

from teams.models import Team

from .models import Channel


class MemberView(View):
    def post(self, request):
        event = json.loads(request.body)
        event_data = event["event"]

        team = Team.objects.get(team_id=event["team_id"])

        if team.bot_user_id == event_data["user"]:
            Channel.objects.create(slack_id=event_data["channel"], team=team)

        return HttpResponse("OK")
