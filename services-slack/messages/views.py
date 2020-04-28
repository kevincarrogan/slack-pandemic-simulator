import json

from django.http import HttpResponse
from django.views import View

from channels.models import Channel
from members.models import Member
from teams.models import Team

from .models import Message


class MessageView(View):
    def post(self, request):
        event = json.loads(request.body)
        event_data = event["event"]

        if event_data.get("subtype"):
            return HttpResponse("NOT CREATED")

        team = Team.objects.get(team_id=event["team_id"])
        channel = Channel.objects.get(slack_id=event_data["channel"], team=team)
        member = Member.objects.get(slack_id=event_data["user"])

        Message.objects.create(
            channel=channel, member=member, slack_timestamp=event_data["ts"],
        )

        return HttpResponse("OK")
