import aioredis
from aioredis.lock import Lock
from time import time
from channels.layers import get_channel_layer
from ..game.game_logic import setup_game
import pickle

redis = None  # Global Redis connection object

async def get_redis_connection():
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://127.0.0.1:6379", decode_responses=True)
    return redis

async def get_number_of_player_from_a_game(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # 10-second lock
    try:
        async with lock:
            game_data = redis.hgetall(f"gameid:{game_id}")
            number_of_players = eval(game_data["players"])
            return number_of_players
    except Exception as e:
        print(f"could not get number of players from game {game_id}, error: {e}")

async def create_game_in_redis():
    print("Creating a game in redis!")
    redis = await get_redis_connection()

    # Generate unique game ID (atomic increment)
    game_id = await redis.incr("game_id_counter")

    # Initialize game state
    game_data = {
        "game_id": str(game_id),
        "players": "[]",
        "state": "open",  # Can be 'open', 'started', 'full'
        "group_name": f"lobby_{game_id}",
    }

    # Save game data to Redis
    await redis.hset(f"game:{game_id}", mapping=game_data)
    return game_id

async def update_last_seen(game_id, player_name):
    print("Updating last seen")
    redis = await get_redis_connection()
    now = time()
    await redis.hset(f"heartbeat:{game_id}", player_name, now)

async def add_player_to_game(player_name, game_id):
    print("Trying to add player to game....")
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
        print(f"Error: {e}")
    return "success"

async def start_game(game_id, game):
    redis = await get_redis_connection()
    lock = Lock(redis, f"game:{game_id}", timeout=10)
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            status = game_data["status"]
            if status == "full" or status == "open":
                await redis.hset(f"game:{game_id}", "status", "started")
                result = setup_player_resources(game_id, game)
                return "ok"
            else:
                return "failed"

    except Exception as e:
        print(f"error {e}")

async def get_player_websockets(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)  # 10-second lock
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            players = eval(game_data["players"])
            websockets = []
            for player in players:
                try:
                    player_websocket_channel_name = await redis.hget(f"websocket_info:{player}", "channel_name")
                    websockets.append(player_websocket_channel_name)
                except Exception as e:
                    print(f"Could not get websockets: {e}")
            return websockets
    except Exception as e:
        raise print(f"Could not get websockets from game {game_id}")
        

async def add_player_websocket_group(game_id, player_name, group_name, channel_name):
    redis = await get_redis_connection()
    await redis.hset(f"websocket_info:{player_name}", 'channel_name', channel_name) # needs to be cleared after the game
    await redis.hset(f"websocket_info:{player_name}", 'group_name', group_name)

async def remove_player_from_channels_websocket_group(player_name):
    redis = await get_redis_connection()
    channel_layer = await get_channel_layer()
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
    return "ok"

async def insert_game_into_redis(game_id, game):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            serialized_game = pickle.dumps(game)
            redis.hset(f"game:{game_id}", "game", serialized_game)
    except Exception as e:
        print(f"Could not insert game into redis error: {e}")
            
async def get_game_from_redis(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            serialized_game = await redis.hget(f"game:{game_id}", "game")
            game = pickle.loads(serialized_game)
            return game
    except Exception as e:
        print("could not get game from redis")

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
            "status": lobby_data.get("state", "open"),  # Assuming a "status" field exists
    })
    print(lobbies)
    return lobbies

async def setup_player_resources(game_id, game):
    redis = await get_redis_connection()
    game_data = await redis.hgetall(f"game:{game_id}")
    player_names = eval(game_data["players"])
    for player, player_name in zip(game.players, player_names):
        if player.wonder == "Colossus of Rhodes": 
            redis.hset(f"game:{game_id}:{player_name}", "ore", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Colossus of Rhodes")
        elif player.wonder == "Colossus of Rhodes Night":
            redis.hset(f"game:{game_id}:{player_name}", "ore", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Colossus of Rhodes Night")
        elif player.wonder == "Lighthouse of Alexandria":
            redis.hset(f"game:{game_id}:{player_name}", "glass", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Lighthouse of Alexandria")
        elif player.wonder == "Lighthouse of Alexandria Night":
            redis.hset(f"game:{game_id}:{player_name}", "glass", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Lighthouse of Alexandria Night")
        elif player.wonder == "Temple of Artemis in Ephesus":
            redis.hset(f"game:{game_id}:{player_name}", "papyrus", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Temple of Artemis in Ephesus")
        elif player.wonder == "Temple of Artemis in Ephesus Night":
            redis.hset(f"game:{game_id}:{player_name}", "papyrus", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Temple of Artemis in Ephesus Night")
        elif player.wonder == "Hanging Gardens of Babylon":
            redis.hset(f"game:{game_id}:{player_name}", "clay", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Hanging Gardens of Babylon")
        elif player.wonder == "Hanging Gardens of Babylon Night":
            redis.hset(f"game:{game_id}:{player_name}", "clay", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Hanging Gardens of Babylon Night")
        elif player.wonder == "Statue of Zeus in Olympia":
            redis.hset(f"game:{game_id}:{player_name}", "wood", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Statue of Zeus in Olympia")
        elif player.wonder == "Statue of Zeus in Olympia Night":
            redis.hset(f"game:{game_id}:{player_name}", "wood", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Statue of Zeus in Olympia Night")
        elif player.wonder == "Mausoleum of Halicarnassus":
            redis.hset(f"game:{game_id}:{player_name}", "cloth", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Mausoleum of Halicarnassus")
        elif player.wonder == "Mausoleum of Halicarnassus Night":
            redis.hset(f"game:{game_id}:{player_name}", "cloth", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Mausoleum of Halicarnassus Night")
        elif player.wonder == "Pyramids of Giza":
            redis.hset(f"game:{game_id}:{player_name}", "stone", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Pyramids of Giza")
        elif player.wonder == "Pyramids of Giza Night":
            redis.hset(f"game:{game_id}:{player_name}", "stone", "1")
            redis.hset(f"game:{game_id}:{player_name}", "wonder", "Pyramids of Giza Night")
        else:
            raise Exception("Error during resource setup")
