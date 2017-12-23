from .models import Connection
from otree.models import  Participant
def ws_connect(message, participant_code):
    participant=Participant.objects.get(code=participant_code)
    new_connection=participant.connection_set.create(event_type='connected')
    print(new_connection)
    print('Participant {participant} connected'.format(participant=participant_code))



def ws_message(message, participant_code):
    ...


# Connected to websocket.disconnect
def ws_disconnect(message, participant_code):
    participant = Participant.objects.get(code=participant_code)
    print('Participant {participant} disconnected'.format(participant=participant_code))
    new_connection=participant.connection_set.create(event_type='disconnected')
    print(new_connection)
