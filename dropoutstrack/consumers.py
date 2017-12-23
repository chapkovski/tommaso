from .models import Connection, Group as OtreeGroup
from channels import Group
import json

from otree.models import Participant


def ws_connect(message, participant_code, group_pk):
    participant = Participant.objects.get(code=participant_code)
    new_connection = participant.connection_set.create(event_type='connected')


def ws_message(message, participant_code, group_pk):
    ...


def ws_disconnect(message, participant_code, group_pk):
    participant = Participant.objects.get(code=participant_code)
    new_connection = participant.connection_set.create(event_type='disconnected')
    group = OtreeGroup.objects.get(pk=group_pk)
    if group.has_dropouts():
        textforgroup = {'group_has_dropouts': 'yes'}
        Group('group{}'.format(group_pk)).send({
            "text": json.dumps(textforgroup),
        })


def wait_page_connect(message, group_pk):
    Group('group{}'.format(group_pk)).add(message.reply_channel)


def wait_page_disconnect(message, group_pk):
    Group('group{}'.format(group_pk)).discard(message.reply_channel)
