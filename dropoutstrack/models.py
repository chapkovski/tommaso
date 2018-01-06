from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django.db import models as djmodels
from otree.models import Participant
import datetime

author = 'Philipp Chapkovski'

doc = """
This app tracks the dropouts. If someone in a group closes the page without submitting it, the entire group
is redirected to the final page.

"""


class Constants(BaseConstants):
    name_in_url = 'dropoutstrack'
    players_per_group = 2
    num_rounds = 1
    threshold_sec = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    is_dropout = models.BooleanField()

    def has_dropouts(self):
        dropouts = []
        for p in self.get_players():
            dropouts.append(p.is_dropout())
        return any(dropouts)


class Player(BasePlayer):
    def is_dropout(self):
        last_connection = self.participant.connection_set.first()
        thresold_met=False
        if last_connection:
            now = datetime.datetime.now(datetime.timezone.utc)
            diff = (now - last_connection.created_at).total_seconds()
            thresold_met = diff > Constants.threshold_sec and last_connection.event_type == 'disconnected'
        recent_connections = self.participant.connection_set.all()[:2].values_list('event_type', flat=True)
        _is_dropout = thresold_met and \
                      not 'success_post' in recent_connections
        return _is_dropout

    testfield = models.CharField()


class Connection(djmodels.Model):
    class Meta:
        ordering = ['-created_at']

    EVENT_TYPES = [('connected', 'CONNECTED'), ('disconnected', 'DISCONNECTED'), ('success_post', 'SUCCESS_POST')]
    created_at = models.DateTimeField(auto_now_add=True)
    participant = djmodels.ForeignKey(to=Participant)
    event_type = models.CharField(choices=EVENT_TYPES)

    def __str__(self):
        return 'Connection: {} for the participant {}'.format(self.event_type, self.participant.code)
