import aioredis
from aioredis.lock import Lock
import json
from time import time
from channels.layers import get_channel_layer

redis = None  # Global Redis connection object

async def get_redis_connection():
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://127.0.0.1:6379", decode_responses=True)
    return redis

async def get_number_of_player_from_a_game(game_id):
    redis = await get_redis_connection()
    game_data = redis.hgetall(f"gameid:{game_id}")
    number_of_players = eval(game_data["players"])
    return number_of_players

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
    lock = Lock(redis, f"game:{game_id}", timeout=10)  # why is the lock lock:game should it not be game: only?
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

async def start_game(game_id):
    redis = await get_redis_connection()
    lock = Lock()

async def get_player_websockets(game_id):
    redis = await get_redis_connection()
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

async def add_player_websocket_group(game_id, player_name, group_name, channel_name):
    redis = await get_redis_connection()
    await redis.hset(f"websocket_info:{player_name}", 'channel_name', channel_name)
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