from itertools import permutations
from aioredis.lock import Lock
from time import time
from channels.layers import get_channel_layer
from ..game.models import Wonder
from itertools import permutations
from .resolve_cards import add_card_resources_to_player
from .setups import setup_player_resources
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis

import traceback

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

async def sell_card(player_name, game_id, card_name): 
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            cards_to_pick_from = player.cards_to_pick_from
            for i in range(len(cards_to_pick_from)):
                if cards_to_pick_from[i].name == card_name:
                    cards_to_pick_from.pop(i)
                    player.resources["coins"] += 3
                    break
            await insert_game_into_redis(game_id, game, lock)
    except Exception as e:
        print(f"could not sell the card: {card_name}, error: {e}")
        traceback.print_exc()

async def check_if_player_can_build_wonder_stage(player_name, game):
    player = get_player_from_game(game, player_name)
    wonder = player.wonder
    if wonder.stage1 != None and not wonder.stage1.purchased:
        if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage1):
            wonder.stage1.purchased = True
            return "1"
    elif wonder.stage2 != None and not wonder.stage2.purchased:
        if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage2):
            wonder.stage2.purchased = True
            return "2"
    elif wonder.stage3 != None and not wonder.stage3.purchased:
        if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage3):
            wonder.stage3.purchased = True
            return "3"
    elif wonder.stage4 != None and not wonder.stage4.purchased:
        if check_if_player_has_resources_to_build_wonder_stage(player, wonder.stage4):
            wonder.stage4.purchased = True
            return "4"

def check_if_player_has_resources_to_build_wonder_stage(player, stage):
    for resource, amount in stage.items():
        if player.resources[resource] < amount:
            return False
    return True

async def build_wonder_stage(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            return await check_if_player_can_build_wonder_stage(player_name, game)
    except Exception as e:
        print(f"could not build wonder, error: {e}")
        traceback.print_exc()

async def get_player_resources(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            print(f"player_name: {player_name}")
            player = get_player_from_game(game, player_name)
            print(f"before i call get_all_player_resources game: {game} player: {player}")
            return get_all_player_resources(player)
    except Exception as e:
        print(f"could not get player resources, error: {e}")
        traceback.print_exc()

async def get_player_state(player_id, game_id): # need to solve this, get_player_resources does not take player_id
    resources = await get_player_resources(player_id, game_id) # once
    wonder = await get_wonder(player_id, game_id)
    cards = await get_player_cards(player_id, game_id)
    return resources, wonder, cards

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
            print(player_ids, player_id, player_id_left, player_id_right)
            return player_ids, player_id, player_id_left, player_id_right
    except Exception as e:
        print(f"could not get player ids")
        traceback.print_exc()

async def get_wonder(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
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

def insert_temporary_resource(game, player_name, resource, amount):
    player = get_player_from_game(game, player_name)
    player.temporary_resources[resource] += amount

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
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
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

async def get_player_decisions(game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            return game.picking_choices
    except Exception as e:
        print(f"Could not get picking_choices")
        traceback.print_exc()

async def pick_card(game_id, card_name, player_name):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            card_is_added = add_card_to_player(game, player_name, card_name)
            await insert_game_into_redis(game_id, game, lock)
            if card_is_added:
                print(f"{card_name} was added to the players deck!")
                return True
            else:
                raise Exception()

    except Exception as e:
        print(f"Could not pick a card this should not happen, error: {e}")
        traceback.print_exc()

async def get_player_cards(player_name, game_id):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            print(f"August cards: {player.cards}")
            return [card.name for card in player.cards.values()]
    except Exception as e:
        print(f"Could not get cards, error: {e}")
        traceback.print_exc()

def get_card_from_cards_to_pick_from(player, card_name):
    for card in player.cards_to_pick_from:
        if card.name == card_name:
            return card

async def player_can_pick_card(player_name, game_id, card_name):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            card = get_card_from_cards_to_pick_from(player, card_name)
            for player_card_name in player.cards.keys(): # Can not have card with the same name
                if card_name == player_card_name:
                    return False
    
            print(f"{player.name} is trying to pick {card.name}")
            if card.cost:
                if "symbol" in card.cost:
                    if card.cost["symbol"] in player.symbols:
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

            mixed_resources = player.mixed_resources # need to sort out mixed resources
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
    except Exception as e:
        print(f"Could not pick a card, error: {e}")
        traceback.print_exc()

def add_card_to_player(game, player_name, card_name):
    player = get_player_from_game(game, player_name)
    for i, card in enumerate(player.cards_to_pick_from):
        if card.name == card_name:
            add_card_resources_to_player(card, player)
            card = player.cards_to_pick_from.pop(i)
            player.cards[card.name] = card
            return True
    return False

def get_player_from_game(game, name):
    print("In get_player_from_game")
    for player in game.players:
        print(f"player.name: {player.name} and name: {name}")
        if player.name == name:
            return player

async def insert_player_choice_into_game(player_name, game_id, choice):
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            game.picking_choices[player_name] = choice
            await insert_game_into_redis(game)
    except Exception as e:
        print(f"Could not get cards, error: {e}")
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