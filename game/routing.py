from django.urls import re_path
from game.channels.consumers import GameConsumer
from game.channels.consumers import LandingPageConsumer

websocket_urlpatterns = [
    re_path(r'ws/lobby/(?P<game_id>[0-9]+)/(?P<player_name>\w+)/?$', GameConsumer.as_asgi()),
    re_path(r'ws/games/', LandingPageConsumer.as_asgi()),
]