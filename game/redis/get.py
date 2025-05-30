import traceback
from aioredis.lock import Lock
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis
import copy

async def get_wonder_based_on_player_id(player_id, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_based_on_player_id(game, player_id)
            wonder = player.wonder
            wonder_name = wonder.name
            if wonder.stage4 != None and wonder.stage4.purchased == True:
                return {"stage": "4", "name":wonder_name}
            elif wonder.stage3 != None and wonder.stage3.purchased == True:
                return {"stage": "3", "name":wonder_name}
            elif wonder.stage2 != None and wonder.stage2.purchased == True:
                return {"stage": "2", "name":wonder_name}
            elif wonder.stage1 != None and wonder.stage1.purchased == True:
                return {"stage": "1", "name":wonder_name}
            else:
                return {"stage": "0", "name":wonder_name}
    except Exception as e:
        print(f"could not get player resources, error: {e}")
        traceback.print_exc()

async def get_player_resources(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            return get_all_player_resources(player)
    except Exception as e:
        print(f"could not get player resources, error: {e}")
        traceback.print_exc()

async def get_player_resources_based_on_player_id(player_id, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_based_on_player_id(game, player_id)
            return get_all_player_resources(player)
    except Exception as e:
        print(f"could not get player resources, error: {e}")
        traceback.print_exc()

async def get_player_tradeable_resources_based_on_player_id(player_id, game_id):
    print("in get_player_tradeable_resources!")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_based_on_player_id(game, player_id)
            resources = get_all_player_resources(player)
            print(f"resources: {resources}")
            cards = player.cards
            print(f"cards: {cards}")
            if any(card.startswith("caravansery") for card in cards):
                resources["mixed_resources"].remove({"wood": 1, "ore": 1, "clay": 1, "stone": 1})
            if any(card.startswith("forum") for card in cards):
                resources["mixed_resources"].remove({"glass": 1, "papyrus": 1, "cloth": 1})
            wonder = player.wonder
            if wonder.name == "Alexandria_day.png":
                if wonder.stage2.purchased:
                    resources["mixed_resources"].remove({"wood": 1, "ore": 1, "clay": 1, "stone": 1})
            if wonder.name == "Alexandria_night.png":
                if wonder.stage1.purchased:
                    resources["mixed_resources"].remove({"wood": 1, "ore": 1, "clay": 1, "stone": 1})
                if wonder.stage2.purchased:
                    resources["mixed_resources"].remove({"glass": 1, "papyrus": 1, "cloth": 1})
            print(f"resources before returning: {resources}")
            return resources

    except Exception as e:
        print(f"could not get player resources, error: {e}")
        traceback.print_exc()

async def get_player_state(player_id, game_id):
    resources = await get_player_resources_based_on_player_id(player_id, game_id)
    wonder = await get_wonder_based_on_player_id(player_id, game_id)
    cards = await get_player_cards_based_on_player_id(player_id, game_id)
    return resources, wonder, cards

def get_player_based_on_player_id(game, player_id):
    for player in game.players:
        if player.player_id == player_id:
            return player

async def get_player_ids(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player_ids = [player.player_id for player in game.players]
            player = get_player_from_game(game, player_name)
            player_id = player.player_id
            player_id_left = player.left_player.player_id
            player_id_right = player.right_player.player_id
            return player_ids, player_id, player_id_left, player_id_right
    except Exception as e:
        print(f"could not get player ids")
        traceback.print_exc()

def get_all_player_resources(player):
    resources = player.resources
    resources["symbols"] = []
    for symbol in player.symbols.keys():
        resources["symbols"].append(symbol)
    resources["mixed_resources"] = player.mixed_resources
    resources["victory_token"] = player.victory_token
    resources["victory_points"] = player.victory_points
    resources["defeat_token"] = player.defeat_token
    resources["millitary_strength"] = player.millitary_strength
    return resources

async def get_player_channel_names(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
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
        
async def get_and_reset_player_decisions(game_id):
    print("in get_player_decisions!")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            picking_choices = copy.deepcopy(game.picking_choices)
            for player_name in game.picking_choices.keys():
                game.picking_choices[player_name] = None
            await insert_game_into_redis(game_id, game, lock)
            return picking_choices
    except Exception as e:
        print(f"Could not get picking_choices")
        traceback.print_exc()

async def get_player_cards(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            return [card.name for card in player.cards.values()]
    except Exception as e:
        print(f"Could not get cards, error: {e}")
        traceback.print_exc()

async def get_player_cards_based_on_player_id(player_id, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_based_on_player_id(game, player_id)
            return [card.name for card in player.cards.values()]
    except Exception as e:
        print(f"Could not get cards, error: {e}")
        traceback.print_exc()

def get_card_from_cards_to_pick_from(player, card_name):
    for card in player.cards_to_pick_from:
        if card.name == card_name:
            return card

def get_player_from_game(game, name):
    for player in game.players:
        if player.name == name:
            return player

def get_player_from_game_based_on_id(game, player_id):
    for player in game.players:
        if player.player_id == player_id:
            return player

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
            "state": lobby_data.get("state", "open"),
    })
    return lobbies

async def get_players(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game_data = await redis.hgetall(f"game:{game_id}")
            number_of_players = game_data["players"] # should be a list
            return eval(number_of_players)
    except Exception as e:
        print(f"could not get players from game {game_id}, error: {e}")
        traceback.print_exc()
