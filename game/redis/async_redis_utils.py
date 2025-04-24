from itertools import permutations
from aioredis.lock import Lock
from time import time
from channels.layers import get_channel_layer
from itertools import permutations
from .resolve_cards import add_card_resources_to_player
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis
from .get import get_player_from_game, get_card_from_cards_to_pick_from

import traceback

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
    print("Selling Card!!!")
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

async def build_wonder_stage(game_id, player_name, wonder_stage):
    print("Building wonder stage!")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=10)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            player = get_player_from_game(game, player_name)
            wonder = player.wonder
            if wonder_stage == "1":
                wonder.stage1.purchased = True # add wh0atever we get from the stages to the players resources. dont forget that
            elif wonder_stage == "2":
                wonder.stage2.purchased = True
            elif wonder_stage == "3":
                wonder.stage3.purchased = True
            elif wonder_stage == "4":
                wonder.stage4.purchased = True
            await insert_game_into_redis(game_id, game, lock)
    except Exception as e:
        print(f"could not build wonder, error: {e}")
        traceback.print_exc()

def insert_temporary_resource(game, player_name, resource, amount):
    player = get_player_from_game(game, player_name)
    player.temporary_resources[resource] += amount

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

async def pick_card(game_id, card_name, player_name):
    print("Picking Card!")
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
    except Exception as e:
        print(f"Could not pick a card this should not happen, error: {e}")
        traceback.print_exc()
        
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
                            use_amount = min(remaining[req], options[req])
                            remaining[req] -= use_amount
                            used_flex.add(i)
                            break

                if all(v <= 0 for v in remaining.values()):
                    return True

            return False
    except Exception as e:
        print(f"Could not pick a card, error: {e}")
        traceback.print_exc()

def add_card_to_player(game, player_name, card_name):
    print("In add_card-to_player")
    player = get_player_from_game(game, player_name)
    for i, card in enumerate(player.cards_to_pick_from):
        print(f"card.name{card.name} card_name : {card_name}")
        if card.name == card_name:
            add_card_resources_to_player(card, player)
            card = player.cards_to_pick_from.pop(i)
            player.cards[card.name] = card
            return True
    return False

async def insert_player_choice_into_game(player_name, game_id, choice):
    print(f"in insert_player_choice, player_name: {player_name} choice: {choice}")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            game.picking_choices[player_name] = choice
            await insert_game_into_redis(game_id, game, lock)
    except Exception as e:
        print(f"Could not get cards, error: {e}")
        traceback.print_exc()