from channels.routing import route
from cms.consumer import http_consumer
from cms.views import on_ws_message

# channel_routing = [
#     route("http.request", "cms.consumers.http_consumer"),
# ]
channel_routing = [route("websocket.receive", on_ws_message), ]
