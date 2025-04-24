def resolve_millitary_conflicts(players, age):
    for i in range(1, len(players)-1, 1):
        calculate_millitary_conflict_points(players[i-1], players[i], players[i+1])
    calculate_millitary_conflict_points(players[-1], players[0], players[1])
    calculate_millitary_conflict_points(players[-2], players[-1], players[0])

def resolve_raw_material(card, player):
    if card.wood > 0:
        player.resources["wood"] += card.wood
    if card.stone > 0:
        player.resources["stone"] += card.stone
    if card.clay > 0:
        player.resources["clay"] += card.clay
    if card.clay > 0:
        player.resources["ore"] += card.ore
    if card.resource_choices:
        for resource_choice in card.resource_choices["choices"]:
            player.mixed_resources.append(resource_choice)

def resolve_manufactured_good(card, player):
    if card.cloth > 0:
        player.resources["cloth"] += card.cloth
    if card.papyrus > 0:
        player.resources["papyrus"] += card.papyrus
    if card.glass > 0:
        player.resources["glass"] += card.glass

def resolve_civilian_structure(card, player):
    if card.victory_points > 0:
        player.victory_points += card.victory_points

def resolve_scientific_structure(card, player):
    if card.compass > 0:
        player.resources["compass"] += card.compass
    if card.gear > 0:
        player.resources["gear"] += card.gear
    if card.tablet > 0:
        player.resources["tablet"] += card.tablet

def resolve_commercial_structure(card, player):
    if card.east_trading:
        player.east_trading = True
    if card.west_trading:
        player.west_trading = True
    if card.marketplace:
        player.marketplace = True
    if card.gold:
        player.resources["coins"] += card.gold
    if card.resource_choices:
        for resource_choice in card.resource_choices["choices"]:
            player.mixed_resources.append(resource_choice)
    if card.gain:
        activity = card.gain["activity"]
        card_colors = ["Red", "Green", "Yellow", "Purple", "Blue", "Brown", "Gray"]
        if activity in card_colors:
            resolve_card_coin_gain(card, player, activity)
        elif activity == "Stage of Wonders":
            resolve_wonder_stage_coins(card, player)

def resolve_wonder_stage_coins(card, player):
        for gain in card.gain["gain"]:
            if gain == "coins":
                multiplier = card.gain["gain"]["coins"]
                player.resources["coins"] += player.stage_of_wonder*multiplier

def resolve_wonder_stage_victory_points(card, player): # used at the end of game
    for gain in card.gain["gain"]:
        if gain == "victory_point":
            multiplier = card.gain["gain"]["victory_point"]
            player.victory_points += player.stage_of_wonder*multiplier

def add_wonder_resources_to_player_inventory(stage, player):
    pass # NEED TO IMPLEMENT THIS!!!!
def add_card_resources_to_player(card, player):
    resolve_card_resources(card, player) # need to sort out resource choices
def resolve_card_coin_gain(card, player, color):
    coins = 0
    for gain in card.gain["gain"]:
        if gain == "coins":
            multiplier = card.gain["gain"]["coins"]
            for location in card.gain["location"]:
                if location == "self":
                    coins += len(player.cards[color])*multiplier
                elif location == "right":
                    coins += len(player.right_player.cards[color])*multiplier
                elif location == "left":
                    coins += len(player.left_player.cards[color])*multiplier
    player["coins"] += coins

def resolve_card_victory_points(card, player, color): # used at the end of game
    victory_points = 0
    for gain in card.gain["gain"]:
        if gain == "victory_point":
            multiplier = card.gain["gain"]["victory_point"]
            for location in card.gain["location"]:
                if location == "self":
                    victory_points += len(player.cards[color])*multiplier
                elif location == "right":
                    victory_points += len(player.right_player.cards[color])*multiplier
                elif location == "left":
                    victory_points += len(player.left_player.cards[color])*multiplier
    player.victory_points += victory_points

def resolve_military_structure(card, player):
    if card.millitary_strength > 0:
        player.millitary_strength += card.millitary_strength

def resolve_guilds(card, player): # This function shold be called at the end of the game. Not done.
    if card.name == "Scientists Guild":
        for mixed_resource in card.resource_choices["choices"]:
            player.mixed_resources.apped(mixed_resource)
    elif card.name == "Builders Guild":
        pass # Resolve when the game ends.
    else:
        pass
        # self.location = location
        # self.activity = activity
        # self.victory_points = victory_points

def resolve_card_resources(card, player):
    print(f"card symbol: {card.name} {card.symbol}")
    for symbol in card.symbol:
        player.symbols[symbol] = True
    if card.color == "Brown":
        resolve_raw_material(card, player)
    elif card.color == "Gray":
        resolve_manufactured_good(card, player)
    elif card.color == "Blue":
        resolve_civilian_structure(card, player)
    elif card.color == "Green":
        resolve_scientific_structure(card, player)
    elif card.color == "Yellow":
        resolve_commercial_structure(card, player)
    elif card.color == "Red":
        resolve_military_structure(card, player)

def calculate_millitary_conflict_points(left_player, player, right_player, age):
    points_per_win = 1
    if age == 2:
        points_per_win = 3
    elif age == 3:
        points_per_win = 5
    if player.millitary_strength > left_player.millitary_strength:
        player.victory_token += points_per_win
    elif player.millitary_strength < left_player.millitary_strength:
        player.defeat_token += 1
    elif player.millitary_strength > right_player.millitary_strength:
        player.victory_token += points_per_win
    elif player.millitary_strength < right_player.millitary_strength:
        player.defeat_token += 1