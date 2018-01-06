from .models import Connection, Group as OtreeGroup, Player
from channels import Group
import json, random

from otree.models import Participant


def ws_connect(message, participant_code, group_pk):
    participant = Participant.objects.get(code=participant_code)
    new_connection = participant.connection_set.create(event_type='connected')


def ws_message(message, participant_code, group_pk):
    player_pk = json.loads(message.content['text']).get('player_pk')
    if player_pk:
        player = Player.objects.get(pk=player_pk)
        player.testfield = random.randint(1, 100)
        player.save()


def ws_disconnect(message, participant_code, group_pk):
    participant = Participant.objects.get(code=participant_code)
    new_connection = participant.connection_set.create(event_type='disconnected')
    group = OtreeGroup.objects.get(pk=group_pk)
    if group.has_dropouts():
        group.is_dropout = True
        group.save()
        textforgroup = {'group_has_dropouts': 'yes'}
        Group('group{}'.format(group_pk)).send({
            "text": json.dumps(textforgroup),
        })


def wait_page_connect(message, group_pk):
    Group('group{}'.format(group_pk)).add(message.reply_channel)


def wait_page_disconnect(message, group_pk):
    Group('group{}'.format(group_pk)).discard(message.reply_channel)
