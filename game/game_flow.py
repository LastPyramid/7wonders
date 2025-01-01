from .redis.async_redis_utils import get_player_websockets, get_number_of_player_from_a_game
from .game.game_logic import setup_game


def start_game(game_id):
    websockets = get_player_websockets(game_id)
    number_of_players = get_number_of_player_from_a_game(game_id)
    if len(websockets) != number_of_players:
        print("amount of websockets connections should be equal to number of players") # add proper handeling later


