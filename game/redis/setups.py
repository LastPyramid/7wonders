from channels.layers import get_channel_layer
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis
from aioredis.lock import Lock
from .resolve_cards import resolve_millitary_conflicts
from ..game.game_logic import start_age_II, start_age_III
import traceback

async def setup_next_age(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            resolve_millitary_conflicts(game.players, game.age)
            game.age += 1
            game.turn = 1
            if game.age == 1:
                pass #setup first turn here as well?
            elif game.age == 2:
                start_age_II(game)
            elif game.age == 3:
                start_age_III(game)
            elif game.age == 4:
                pass # game has ended?
            else:
                raise Exception("AGE CAN NOT BE SOMETHING ELSE OTHER THAN 1, 2, 3")
            await insert_game_into_redis(game_id, game, lock)
            return game
            
    except Exception as e:
        print(f"could not set up new age, error: {e}")
        traceback.print_exc()

async def setup_next_turn(game_id):
    print("setting up next turn!")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            reset_temporary_resources(game)
            game.turn += 1
            if game.age == 2: # anti clockwise
                previous_players_cards = game.players[0].cards_to_pick_from
                temp_cards = []
                for i in range(len(game.players)-1, -1, -1):
                    temp_cards = game.players[i].cards_to_pick_from
                    game.players[i].cards_to_pick_from = previous_players_cards
                    previous_players_cards = temp_cards
            else: # clockwise
                previous_players_cards = game.players[-1].cards_to_pick_from
                temp_cards = []
                for i in range(len(game.players)):
                    temp_cards = game.players[i].cards_to_pick_from
                    game.players[i].cards_to_pick_from = previous_players_cards
                    previous_players_cards = temp_cards
            await insert_game_into_redis(game_id, game, lock)
            return game
    except Exception as e:
        print(f"could not set up new age, error: {e}")
        traceback.print_exc()

async def setup_player_resources(game):
    players = game.players
    for player in players:
        if player.wonder.name == "Rhodos_day.png": 
            player.resources["ore"] += 1
        elif player.wonder.name == "Rhodos_night.png":
            player.resources["ore"] += 1
        elif player.wonder.name == "Alexandria_day.png":
            player.resources["glass"] += 1
        elif player.wonder.name == "Alexandria_night.png":
            player.resources["glass"] += 1
        elif player.wonder.name == "Ephesos_day.png":
            player.resources["papyrus"] += 1
        elif player.wonder.name == "Ephesos_night.png":
            player.resources["papyrus"] += 1
        elif player.wonder.name == "Babylon_day.png":
            player.resources["wood"] += 1
        elif player.wonder.name == "Babylon_night.png":
            player.resources["wood"] += 1
        elif player.wonder.name == "Olympia_day.png":
            player.resources["clay"] += 1
        elif player.wonder.name == "Olympia_night.png":
            player.resources["clay"] += 1
        elif player.wonder.name == "Halikarnassos_day.png":
            player.resources["cloth"] += 1
        elif player.wonder.name == "Halikarnassos_night.png":
            player.resources["cloth"] += 1
        elif player.wonder.name == "Gizah_day.png":
            player.resources["stone"] += 1
        elif player.wonder.name == "Gizah_night.png":
            player.resources["stone"] += 1
        else:
            raise Exception("Error during resource setup")

def reset_temporary_resources(game):
    for player in game.players:
        player.temporary_resources = {"compass": 0, "gear": 0, "tablet": 0, "ore": 0, "stone": 0, "wood": 0, "clay": 0,
                        "papyrus": 0, "cloth": 0, "glass": 0}