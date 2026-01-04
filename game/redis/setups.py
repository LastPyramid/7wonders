from channels.layers import get_channel_layer
from .common import get_redis_connection, get_game_from_redis, insert_game_into_redis
from redis.asyncio.lock import Lock
from .resolve_cards import (resolve_millitary_conflicts, resolve_victory_points_from_commercial_structure,
    resolve_victory_points_from_sientific_structure, resolve_victory_points_from_civilian_structure,
    resolve_victory_points_from_guilds)
from ..game.game_logic import start_age_II, start_age_III
from ..game.models import ScientificStructure

import traceback

async def setup_next_age(game_id):
    print("in setup_next_age")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            resolve_millitary_conflicts(game.players, game.age)
            game.age += 1
            game.turn = 1
            if game.age == 2:
                start_age_II(game)
            elif game.age == 3:
                start_age_III(game)
            elif game.age == 4:
                end_game(game)
            else:
                raise Exception("AGE CAN NOT BE SOMETHING ELSE OTHER THAN 1, 2, 3, 4")
            for player in game.players:
                player.traded = False
                player.temporary_resources = {}
            await insert_game_into_redis(game_id, game, lock)
            return game
            
    except Exception as e:
        print(f"could not set up new age, error: {e}")
        traceback.print_exc()

def end_game(game):
    for player in game.players:
        player.victory_points = calculate_final_scores(player)
        print(f"final score for player: {player} is {player.victory_points}")

def calculate_final_scores(player):
    final_score = 0
    # Points from victory board
    wonder = player.wonder
    if wonder.stage1.purchased:
        if "victory_points" in wonder.stage1.benefit:
            final_score += wonder.stage1.benefit["victory_points"]
        if wonder.stage2.purchased:
            if "victory_points" in wonder.stage2.benefit:
                final_score += wonder.stage2.benefit["victory_points"]
            if wonder.stage3 and wonder.stage3.purchased:
                if "victory_points" in wonder.stage3.benefit:
                    final_score += wonder.stage3.benefit["victory_points"]
                if wonder.stage4 and wonder.stage4.purchased:
                    if "victory_points" in wonder.stage4.benefit:
                        final_score += wonder.stage4.benefit["victory_points"]
    print(f"{player.name} things")
    # Points from Coins
    final_score += int(player.resources["coins"]/3)
    c = int(player.resources["coins"]/3)
    print(f"{c} points from coins")

    # Points from millitary conflicts
    final_score += player.victory_token - player.defeat_token
    print(f"{player.victory_token - player.defeat_token} from milltary conflicts")

    # Points from Blue Cards
    print(player.cards)
    blue_cards = [card for card in player.cards.values() if card.color ==  "Blue"]
    fs = 0
    for card in blue_cards:
        fs += resolve_victory_points_from_civilian_structure(card) #update later
    print(f"{fs} from blue cards")
    final_score += fs

    # Points from Yellow Cards
    yellow_cards = [card for card in player.cards.values() if card.color == "Yellow"]
    fs = 0
    for card in yellow_cards:
        fs += resolve_victory_points_from_commercial_structure(player, card) # Not Done remove when done
    final_score += fs
    print(f"{fs} points from yellow cards")

    # Points from Green Cards
    green_cards = [card for card in player.cards.values() if card.color == "Green"]
    purple_cards = [card for card in player.cards.values() if card.color == "Purple"]
    player_has_science_guild = False
    fs = 0
    for card in purple_cards:
        if card.name == "scientists_guild1":
            player_has_science_guild = True

    if player_has_science_guild: # Testing all choices of [gear, tablet, compass]
        highest_points = 0
        current_points = 0

        compass = ScientificStructure(3, "Green", "3+", "temp_sientific_guild", cost={}, compass=1)
        gear = ScientificStructure(3, "Green", "3+", "temp_sientific_guild", cost={}, gear=1)
        tablet = ScientificStructure(3, "Green", "3+", "temp_sientific_guild", cost={}, tablet=1)
        compass_gear_tablet = [compass, gear, tablet]
        for card in compass_gear_tablet: 
            green_cards.append(card)
            current_points = resolve_victory_points_from_sientific_structure(player, green_cards)
            if current_points > highest_points:
                higest_points = current_points
            green_cards.pop()
        fs += higest_points
    else:
        fs += resolve_victory_points_from_sientific_structure(green_cards)
    final_score += fs

    # Purple Cards
    purple_cards = [card for card in player.cards.values() if card.color == "Purple"]
    fs = 0
    for card in purple_cards:
        fs += resolve_victory_points_from_guilds(card)
    final_score += fs

    return final_score

async def setup_next_turn(game_id):
    print("setting up next turn!")
    redis = await get_redis_connection()
    lock = Lock(redis, f"lock:game:{game_id}", timeout=30)
    try:
        async with lock:
            game = await get_game_from_redis(game_id, lock)
            reset_temporary_resources(game)
            print(f"Going from turn {game.turn} -> {game.turn+1}")
            game.turn += 1
            # if game.turn == 3: # REMOVE
            #     end_game(game) # remove
            #     print(f"ended game!")
            #     for player in game.players:
            #         print(f"Final Score of {player.name} is {player.victory_points}")

            if game.age == 2: # anti clockwise
                previous_players_cards = game.players[0].cards_to_pick_from
                temp_cards = []
                for i in range(len(game.players)-1, -1, -1):
                    temp_cards = game.players[i].cards_to_pick_from
                    game.players[i].cards_to_pick_from = previous_players_cards
                    previous_players_cards = temp_cards
            else: # clockwise
                previous_players_cards = game.players[-1].cards_to_pick_from
                temp_cards = []
                for i in range(len(game.players)):
                    temp_cards = game.players[i].cards_to_pick_from
                    game.players[i].cards_to_pick_from = previous_players_cards
                    previous_players_cards = temp_cards
            for player in game.players:
                print(player.cards.values())
                player.traded = False
                player.temporary_resources = {}
            for card in game.age_II_cards:
                print(card)

            await insert_game_into_redis(game_id, game, lock)
            return game
    except Exception as e:
        print(f"could not set up new age, error: {e}")
        traceback.print_exc()

async def setup_player_resources(game):
    players = game.players
    for player in players:
        if player.wonder.name == "Rhodos_day.png": 
            player.resources["ore"] += 1
        elif player.wonder.name == "Rhodos_night.png":
            player.resources["ore"] += 1
        elif player.wonder.name == "Alexandria_day.png":
            player.resources["glass"] += 1
        elif player.wonder.name == "Alexandria_night.png":
            player.resources["glass"] += 1
        elif player.wonder.name == "Ephesos_day.png":
            player.resources["papyrus"] += 1
        elif player.wonder.name == "Ephesos_night.png":
            player.resources["papyrus"] += 1
        elif player.wonder.name == "Babylon_day.png":
            player.resources["wood"] += 1
        elif player.wonder.name == "Babylon_night.png":
            player.resources["wood"] += 1
        elif player.wonder.name == "Olympia_day.png":
            player.resources["clay"] += 1
        elif player.wonder.name == "Olympia_night.png":
            player.resources["clay"] += 1
        elif player.wonder.name == "Halikarnassos_day.png":
            player.resources["cloth"] += 1
        elif player.wonder.name == "Halikarnassos_night.png":
            player.resources["cloth"] += 1
        elif player.wonder.name == "Gizah_day.png":
            player.resources["stone"] += 1
        elif player.wonder.name == "Gizah_night.png":
            player.resources["stone"] += 1
        else:
            raise Exception("Error during resource setup")

def reset_temporary_resources(game):
    for player in game.players:
        player.temporary_resources = {"compass": 0, "gear": 0, "tablet": 0, "ore": 0, "stone": 0, "wood": 0, "clay": 0,
                        "papyrus": 0, "cloth": 0, "glass": 0}
