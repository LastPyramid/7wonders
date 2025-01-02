from .redis.async_redis_utils import get_player_websockets, get_number_of_player_from_a_game, start_game
from .game.game_logic import setup_game

def start(game_id): # start_game is async so you have to deal with that.
    websockets = get_player_websockets(game_id)
    number_of_players = get_number_of_player_from_a_game(game_id)
    if len(websockets) != number_of_players:
        print("amount of websockets connections should be equal to number of players") # add proper handeling later
    game = setup_game(number_of_players)
    result = start_game(game_id, game)    
    if result == "failed":
        raise Exception("could not start game")
    


