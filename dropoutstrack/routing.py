from channels.routing import route
from .consumers import ws_message, ws_connect, ws_disconnect
from otree.channels.routing import channel_routing
from channels.routing import include

tracking_path = r'^/(?P<participant_code>\w+)$'

tracking_routing = [route("websocket.connect",
                          ws_connect, path=tracking_path),
                    route("websocket.receive",
                          ws_message, path=tracking_path),
                    route("websocket.disconnect",
                          ws_disconnect, path=tracking_path), ]

channel_routing += [
    include(tracking_routing, path=r"^/tracking_channel"),
]
