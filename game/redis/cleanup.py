import asyncio
from time import time
from .async_redis_utils import get_redis_connection, remove_player_from_game, remove_player_from_channels_websocket_group

async def cleanup_stale_users(): # move this to redis function?
    redis = await get_redis_connection()
    while True:
        now = time()
        heartbeats_and_ids = await redis.keys("heartbeat:*")
        game_ids = [entry.split(":")[1] for entry in heartbeats_and_ids]
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print(game_ids)
        for game_id in game_ids:
            players = await redis.hgetall(f"heartbeat:{game_id}")
            for player_name, last_seen in players.items():
                if now - float(last_seen) > 60:
                    await redis.hdel(f"heartbeat:{game_id}", player_name)
                    print("We're doing this thing")
                    await remove_player_from_game(player_name, game_id)
                    await remove_player_from_channels_websocket_group(player_name)

        await asyncio.sleep(30)  # Run every 30 seconds
