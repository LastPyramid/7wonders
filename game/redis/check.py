import traceback
from aioredis.lock import Lock
from ..game.models import Wonder
from .setups import setup_player_resources
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis
from .get import get_player_from_game


async def check_if_everyone_has_picked_a_wonder(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
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

async def check_if_everyone_have_made_a_picking_decision(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            all_players_have_made_a_picking_decision = all(game.picking_choices.values())
            if all_players_have_made_a_picking_decision:
                return game
            else:
                return False
    except Exception as e:
        print(f"could not check if everyone has picked a CARD, error: {e}")
        traceback.print_exc()

def check_if_player_has_resources_to_build_wonder_stage(player, stage):
    for resource, amount in stage.cost.items():
        if player.resources[resource] < amount:
            return False
    return True

async def check_if_player_can_build_wonder_stage(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            wonder = player.wonder
            if wonder.stage1 != None and not wonder.stage1.purchased:
                if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage1):
                    return "1"
            elif wonder.stage2 != None and not wonder.stage2.purchased:
                if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage2):
                    return "2"
            elif wonder.stage3 != None and not wonder.stage3.purchased:
                if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage3):
                    return "3"
            elif wonder.stage4 != None and not wonder.stage4.purchased:
                if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage4):
                    return "4"
            else:
                return False
    except Exception as e:
        print(f"could not build wonder, error: {e}")
        traceback.print_exc()