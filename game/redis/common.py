from ..game.models import Game
from aioredis.lock import Lock
import traceback
import aioredis

redis = None  # Global Redis connection object

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

async def get_redis_connection():
    global redis
    if not redis:
        redis = await aioredis.from_url("redis://127.0.0.1:6379", decode_responses=True)
    return redis

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