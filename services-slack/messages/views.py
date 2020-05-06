import datetime
import json

from django.conf import settings
from django.http import HttpResponse
from django.views import View

from channels.models import Channel
from members.models import Member
from teams.models import Team

from services_slack.services import service_request

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

        slack_timestamp = event_data["ts"]

        message = Message.objects.create(
            channel=channel, member=member, slack_timestamp=slack_timestamp,
        )
        timestamp, _ = slack_timestamp.split(".")
        timestamp = int(timestamp)
        message_time = datetime.datetime.fromtimestamp(timestamp)

        overlapping_messages = Message.objects.filter(
            timestamp__gte=message_time - settings.CONTACT_TIMEDELTA,
            timestamp__lte=message_time,
        ).exclude(pk=message.pk,)

        for overlapping_message in overlapping_messages:
            members = [message.member, overlapping_message.member]
            people_ids = [str(member.person_id) for member in members]

            service_request("contact", "/contact/", {"people_ids": people_ids,})

        return HttpResponse("OK")
