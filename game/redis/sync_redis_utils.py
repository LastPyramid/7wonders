import redis
import json
import os

REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

redis_client = None

def get_redis_connection():
    global redis_client
    if not redis_client:
        redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return redis_client

def get_lobbies():
    redis = get_redis_connection()
    keys = redis.keys("game:*")  # Get all game keys
    lobbies = []

    for key in keys:
        lobby_data = redis.hgetall(key)
        amount_of_players = len(eval(lobby_data.get("players", "[]")))

        lobbies.append({
            "game_id": key.split(":")[1],  # Extract game_id from key
            "players": amount_of_players,
            "status": lobby_data.get("state", "open"),  # Assuming a "status" field exists
    })

    return lobbies
