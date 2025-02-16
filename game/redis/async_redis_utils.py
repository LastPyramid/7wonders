import aioredis
from aioredis.lock import Lock
from time import time
from channels.layers import get_channel_layer
from ..game.models import Game, Wonder
from ..game.game_logic import start_age_II, start_age_III
from itertools import permutations

import traceback

redis = None  # Global Redis connection object

async def get_redis_connection():
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://127.0.0.1:6379", decode_responses=True)
    return redis

async def get_players(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # 10-second lock
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            number_of_players = game_data["players"] # should be a list
            return eval(number_of_players)
    except Exception as e:
        print(f"could not get players from game {game_id}, error: {e}")
        traceback.print_exc()

async def create_game_in_redis():
    redis = await get_redis_connection()

    # Generate unique game ID (atomic increment)
    game_id = await redis.incr("game_id_counter")

    # Initialize game state
    game_data = {
        "game_id": str(game_id),
        "players": "[]",
        "state": "open",  # Can be 'open', 'full', 'picking', age1, age2,age3 ?
        "group_name": f"lobby_{game_id}",
    }

    # Save game data to Redis
    await redis.hset(f"game:{game_id}", mapping=game_data)
    return game_id

async def update_last_seen(game_id, player_name):
    redis = await get_redis_connection()
    now = time()
    await redis.hset(f"heartbeat:{game_id}", player_name, now)

async def add_player_to_game(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # why is the lock lock:game should it not be game: only?
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            players = eval(game_data["players"])
            print(f"These players:{players} exist at the moment in game{game_id}")
            if len(players) < 7:
                players.append(player_name)
                await redis.hset(f"game:{game_id}", "players", str(players))
                if len(players) >= 7:
                    await redis.hset(f"game:{game_id}", "state", "full")
            else:
                return "full"
    except Exception as e:
        print(f"add_player_to_game fails, Error: {e}")
        traceback.print_exc()
    return "success"

async def lock_game(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            status = game_data["state"]
            if status == "full" or status == "open":
                await redis.hset(f"game:{game_id}", "state", "picking")
                return "ok"
            else:
                return "failed"

    except Exception as e:
        print(f"error while trying to lock_game, Error: {e}")
        traceback.print_exc()

async def get_player_channel_names(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # 10-second lock
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            players = eval(game_data["players"])
            websockets = {}
            for player in players:
                try:
                    player_websocket_channel_name = await redis.hget(f"websocket_info:{player}", "channel_name")
                    websockets[player] = player_websocket_channel_name
                except Exception as e:
                    print(f"Could not get websockets: {e}")
                    traceback.print_exc()
            return websockets
    except Exception as e:
        print(f"Could not get websockets from game {game_id}, error: {e}")
        traceback.print_exc()
        
async def add_player_websocket_group(game_id, player_name, group_name, channel_name):
    redis = await get_redis_connection()
    await redis.hset(f"websocket_info:{player_name}", 'channel_name', channel_name) # needs to be cleared after the game
    await redis.hset(f"websocket_info:{player_name}", 'group_name', group_name)

async def remove_player_from_channels_websocket_group(player_name):
    redis = await get_redis_connection()
    channel_layer = get_channel_layer()
    channels_data = await redis.hgetall(f"websocket_info:{player_name}")
    channel_name = channels_data['channel_name']
    group_name = channels_data['group_name']
    await channel_layer.group_discard(group_name, channel_name)
    await channel_layer.group_send(
            group_name,
            {
                "type": "chat_message",
                "message": f"{player_name} was removed due to stale connection"
            }
    )

async def remove_player_from_game(player_name, game_id):
    print("Removing player from game...")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # 10-second lock
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            players = eval(game_data["players"])
            print(f"These players:{players} exist at the moment in game{game_id}")
            players = [name for name in players if name != player_name]
            print(f"Did he get removed? {players} ")
            await redis.delete(f"websocket_info:{player_name}")
            await redis.hset(f"game:{game_id}", "players", str(players))
            if len(players) < 7:
                await redis.hset(f"game:{game_id}", "state", "open")
    except Exception as e:
        print(f"Could not remove player:{player_name} {e}")
        traceback.print_exc()
    return "ok"

async def insert_game_into_redis(game_id, game, lock=None):
    redis = await get_redis_connection()
    if not lock:
        print("had to create a lock in insert_game_into_redis")
        lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
        async with lock:
            serialized_game = str(Game.to_dict(game))
            await redis.hset(f"game:{game_id}", "game", serialized_game)
    try:
        serialized_game = str(Game.to_dict(game))
        await redis.hset(f"game:{game_id}", "game", serialized_game)
    except Exception as e:
        print(f"Could not insert game into redis error: {e}")
        traceback.print_exc()

async def pick_wonder(game_id, player_name, wonder_name):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            print("PICK WONDER has the LOCK")
            game = await get_game_from_redis(game_id, lock)
            for player in game.players:
                if player.name == player_name:
                    for w in player.wonder:
                        if wonder_name == w.name:
                            player.wonder = w # exception if this does not happen?
            await insert_game_into_redis(game_id, game, lock)
    except Exception as e:
        print(f"Could not alter the game and insert pick_wonder, error: {e}")
        traceback.print_exc()

async def check_if_everyone_has_picked_a_wonder(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    print("CHECK_IF_EVERYONE_HAS_PICKED has THE LOCK")
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            for player in game.players:
                if not isinstance(player.wonder, Wonder):
                    return False
                if player.wonder.name not in ["Rhodos_day.png", "Rhodos_night.png", "Alexandria_day.png", "Alexandria_night.png", "Ephesos_day.png", "Ephesos_night.png", "Babylon_day.png", "Babylon_night.png", "Olympia_day.png", "Olympia_night.png", "Halikarnassos_day.png", "Halikarnassos_night.png", "Gizah_day.png", "Gizah_night.png"]:
                    return False
            await setup_player_resources(game) # Ready to start
            await insert_game_into_redis(game_id, game, lock)
            return game
    except Exception as e:
        print(f"could not check if everyone has picked a wonder, error: {e}")
        traceback.print_exc()

async def check_if_everyone_has_picked_a_card(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            number_of_unpicked_cards = 7 - game.turn
            for player in game.players:
                if number_of_unpicked_cards != player.card_to_pick_from:
                    return False
            return True
    except Exception as e:
        print(f"could not check if everyone has picked a CARD, error: {e}")
        traceback.print_exc()

async def pick_card(game_id, card_name, player_name):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            card_is_added = add_card_to_player(game, player_name, card_name)
            await insert_game_into_redis(game)
            if card_is_added:
                print(f"{card_name} was added to the players deck!")
                return True
            else:
                print("something went wrong adding card to the players deck")
                return False

    except Exception as e:
        print(f"Could not pick a card, error: {e}")
        traceback.print_exc()

async def get_player_resources(game_id, player_name):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            resources = player.resources
            await insert_game_into_redis(game)
            return resources
    except Exception as e:
        print(f"Could not pick a card, error: {e}")
        traceback.print_exc()
        
def mixed_resources(player):
    pass

from itertools import permutations

async def player_can_pick_card(card, player):
    if card.symbol in player.symbols:
        return True

    required_resources = card.cost.copy()
    resources_to_remove = []
    
    for resource, amount in required_resources.items():
        if resource in player.resources:
            if player.resources[resource] >= amount:
                resources_to_remove.append(resource)
            else:
                required_resources[resource] -= player.resources[resource]

    for resource in resources_to_remove:
        del required_resources[resource]

    if not required_resources:
        return True

    mixed_resources = player.mixed_resources
    required_list = list(required_resources.keys())

    for resource_perm in permutations(required_list):
        remaining = required_resources.copy()
        used_flex = set()

        for req in resource_perm:
            for i, options in enumerate(mixed_resources):
                if req in options and i not in used_flex:
                    remaining[req] -= 1
                    used_flex.add(i)
                    break

        if all(v <= 0 for v in remaining.values()):
            return True

    return False

def add_card_to_player(game, player_name, card_name):
    player = get_player_from_game(game, player_name)
    for i, card in enumerate(player.card_to_pick_from):
        if card.name == card_name:
            if player_can_pick_card(card, player):
                player.cards.append(player.card_to_pick_from.pop(i))
                return True
    return False

def get_player_from_game(game, name):
    for player in game.players:
        if player.name == name:
            return player

async def get_game_from_redis(game_id, lock):
    if lock == None:
        raise Exception("lock is None in get_game_from_redis")
    print("GET_GAME_FROM_REDIS has the LOCK")
    redis = await get_redis_connection()
    try:
        string_game = await redis.hget(f"game:{game_id}", "game")
        dict_game = eval(string_game)
        deserialized_game = Game.from_dict(dict_game)
        return deserialized_game
    except Exception as e:
        print(f"could not get game from redis, error: {e}")
        traceback.print_exc()

async def get_lobbies():
    redis = await get_redis_connection()
    keys = await redis.keys("game:*")  # Get all game keys
    lobbies = []

    for key in keys:
        lobby_data = await redis.hgetall(key)
        players = eval(lobby_data.get("players", "[]"))
        print(f"lobby: {key}, players: {players}")

        lobbies.append({
            "game_id": key.split(":")[1],  # Extract game_id from key
            "players": players,
            "state": lobby_data.get("state", "open"),  # Assuming a "status" field exists
    })
    return lobbies

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
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            game.turn += 1
            if game.age % 2 != 0: # clockwise
                previous_players_cards = []
                temp_cards = []
                for i in range(len(game.players)-1, -1, -1):
                    temp_cards = game.players[i].cards
                    game.players[i].cards = previous_players_cards
                    previous_players_cards = temp_cards
                game.players[len(game.players)].cards = previous_players_cards
            else: # anti-clockwise
                previous_players_cards = []
                temp_cards = []
                for i in range(len(game.players)):
                    temp_cards = game.players[i].cards
                    game.players[i].cards = previous_players_cards
                    previous_players_cards = temp_cards
                game.players[0].cards = previous_players_cards
            await insert_game_into_redis(game_id, game, lock)
            return game
    except Exception as e:
        print(f"could not set up new age, error: {e}")
        traceback.print_exc()

def resolve_millitary_conflicts(players, age):
    for i in range(1, len(players)-1, 1):
        calculate_millitary_conflict_points(players[i-1], players[i], players[i+1])
    calculate_millitary_conflict_points(players[-1], players[0], players[1])
    calculate_millitary_conflict_points(players[-2], players[-1], players[0])

def calculate_millitary_conflict_points(left_player, player, right_player, age):
    points_per_win = 1
    if age == 2:
        points_per_win = 3
    elif age == 3:
        points_per_win = 5
    if player.millitary_strength > left_player.millitary_strength:
        player.victory_token += points_per_win
    elif player.millitary_strength < left_player.millitary_strength:
        player.defeat_token += 1
    elif player.millitary_strength > right_player.millitary_strength:
        player.victory_token += points_per_win
    elif player.millitary_strength < right_player.millitary_strength:
        player.defeat_token += 1

def get_player_from_game(game, name):

    pass

async def setup_player_resources(game):
    players = game.players
    for player in players:
        if player.wonder.name == "Rhodos_day.png": 
            player.resources.ore += 1
        elif player.wonder.name == "Rhodos_night.png":
            player.resources.ore += 1
        elif player.wonder.name == "Alexandria_day.png":
            player.resources.glass += 1
        elif player.wonder.name == "Alexandria_night.png":
            player.resources.glass += 1
        elif player.wonder.name == "Ephesos_day.png":
            player.resources.papyrus += 1
        elif player.wonder.name == "Ephesos_night.png":
            player.resources.papyrus += 1
        elif player.wonder.name == "Babylon_day.png":
            player.resources.wood += 1
        elif player.wonder.name == "Babylon_night.png":
            player.resources.wood += 1
        elif player.wonder.name == "Olympia_day.png":
            player.resources.clay += 1
        elif player.wonder.name == "Olympia_night.png":
            player.resources.clay += 1
        elif player.wonder.name == "Halikarnassos_day.png":
            player.resources.cloth += 1
        elif player.wonder.name == "Halikarnassos_night.png":
            player.resources.cloth += 1
        elif player.wonder.name == "Gizah_day.png":
            player.resources.stone += 1
        elif player.wonder.name == "Gizah_night.png":
            player.resources.stone += 1
        else:
            raise Exception("Error during resource setup")
