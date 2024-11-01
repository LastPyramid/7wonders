from ..game.models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure
# add game logic here and import shit fro models.py
#
def generate_age_I_cards(nr_of_players):
    if nr_of_players < 3:
        print("too few players")
    else:
        return generate_age_I_raw_material_cards() + generate_age_I_manufactured_goods() + generate_age_I_civilian_structures() + generate_age_I_scientific_structures() + generate_age_I_commerical_structures(nr_of_players) + generate_age_I_millitary_structures(nr_of_players)

def generate_age_I_raw_material_cards(): # should we add cost as 0 or let it be None?
    lumber_yard1 = RawMaterial(1, "Brown", "3+", "Lumber Yard", wood = 1)
    lumber_yard2 = RawMaterial(1, "Brown", "3+", "Lumber Yard", wood = 1)

    clay_pool1 = RawMaterial(1, "Brown", "3+", "Clay Pool", clay = 1)
    clay_pool2 = RawMaterial(1, "Brown", "3+", "Clay Pool", clay = 1)

    stone_pit1 = RawMaterial(1, "Brown", "3+", "Stone Pit", stone = 1)
    stone_pit2 = RawMaterial(1, "Brown", "3+", "Stone Pit", stone = 1)

    ore_vein1 = RawMaterial(1, "Brown", "3+", "Ore Vein", ore = 1)

    return  [lumber_yard1, lumber_yard2, clay_pool1, clay_pool2, stone_pit1, stone_pit2, ore_vein1]

def generate_age_I_manufactured_goods():
    glassworks = ManufacturedGood(1, "Grey", "3+", "Glassworks", glass = 1)
    loom = ManufacturedGood(1, "Grey", "3+", "Loom", cloth = 1)
    press = ManufacturedGood(1, "Grey", "3+", "Press", papyrus = 1)

    return [glassworks, press, loom]

def generate_age_I_civilian_structures():
    altar1 = CivilianStructure(1, "Blue", "3+", "Altar", victory_points=2)
    altar2 = CivilianStructure(1, "Blue", "3+", "Altar", victory_points=2)

    baths1 = CivilianStructure(1, "Blue", "3+", "Baths", victory_points=3)
    baths2 = CivilianStructure(1, "Blue", "3+", "Baths", victory_points=3)

    return [altar1, altar2, baths1, baths2]

def generate_age_I_scientific_structures():
    apothecary1 = ScientificStructure(1, "Green", "3+", "Apothecary", compass=1)
    apothecary2 = ScientificStructure(1, "Green", "3+", "Apothecary", compass=1)

    workshop1 = ScientificStructure(1, "Green", "3+", "Workshop", gear=1)
    workshop2 = ScientificStructure(1, "Green", "3+", "Workshop", gear=1)

    scriptorium1 = ScientificStructure(1, "Green", "3+", "Scriptorium", tablet=1)

    return [apothecary1, apothecary2, workshop1, workshop2, scriptorium1]

def generate_age_I_commerical_structures(nr_of_players):
    east_trading_post1 = CommercialStructure(1, "Yellow", "3+", "East Trading Post", east_trading=True)
    east_trading_post2 = CommercialStructure(1, "Yellow", "3+", "East Trading Post", east_trading=True)

    west_trading_post1 = CommercialStructure(1, "Yellow", "3+", "West Trading Post", west_trading=True)
    west_trading_post2 = CommercialStructure(1, "Yellow", "3+", "West Trading Post", west_trading=True)

    tavern = CommercialStructure(1, "Yellow", "4+", "Tavern", gold=5)
    marketplace1 = CommercialStructure(1, "Yellow", "4+", "Marketplace", marketplace=True)
    marketplace2 = CommercialStructure(1, "Yellow", "4+", "Marketplace", marketplace=True)

    three_players = [east_trading_post1, east_trading_post2, west_trading_post1, west_trading_post2]
    if nr_of_players > 3:
        return three_players + [tavern, marketplace1, marketplace2]
    return three_players

def generate_age_I_millitary_structures(nr_of_players):
    stockade1 = MilitaryStructure(1, "Red", "3+", "Stockade", {"wood": 1}, shield=1)
    stockade2 = MilitaryStructure(1, "Red", "3+", "Stockade", {"wood": 1}, shield=1)

    barracks1 = MilitaryStructure(1, "Red", "3+", "Barracks", {"ore": 1}, shield=1)
    barracks2 = MilitaryStructure(1, "Red", "3+", "Barracks", {"ore": 1}, shield=1)

    guard_tower1 = MilitaryStructure(1, "Red", "4+", "Guard Tower", {"clay": 1}, shield=1)
    guard_tower2 = MilitaryStructure(1, "Red", "4+", "Guard Tower", {"clay": 1}, shield=1)

    three_players = [stockade1, stockade2, barracks1, barracks2]
    if nr_of_players > 3:
        return three_players + [guard_tower1, guard_tower2]
    return three_players
