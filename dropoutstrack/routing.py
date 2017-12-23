from channels.routing import route
from .consumers import ws_message, ws_connect, ws_disconnect, wait_page_connect, wait_page_disconnect
from otree.channels.routing import channel_routing
from channels.routing import include

tracking_path = r'^/(?P<participant_code>\w+)/(?P<group_pk>\w+)$'
wp_path = r'^/(?P<group_pk>\w+)$'
tracking_routing = [route("websocket.connect",
                          ws_connect, path=tracking_path),
                    route("websocket.receive",
                          ws_message, path=tracking_path),
                    route("websocket.disconnect",
                          ws_disconnect, path=tracking_path), ]

wait_page_routing = [route("websocket.connect",
                           wait_page_connect, path=wp_path),
                    route("websocket.disconnect",
                          wait_page_disconnect, path=wp_path), ]

channel_routing += [
    include(tracking_routing, path=r"^/tracking_channel"),
    include(wait_page_routing, path=r"^/wp_channel"),
]
