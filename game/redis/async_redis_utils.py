import aioredis
from aioredis.lock import Lock
from time import time
from channels.layers import get_channel_layer
from ..game.models import Game, Wonder
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
            return game
    except Exception as e:
        print(f"could not check if everyone has picked a wonder, error: {e}")
        traceback.print_exc()

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
