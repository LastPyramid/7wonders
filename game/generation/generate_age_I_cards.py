from ..game.models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure
# add game logic here and import shit fro models.py
#
def generate_age_I_cards(nr_of_players):
    if nr_of_players < 3:
        print("too few players")
    else:
        return generate_age_I_raw_material_cards(nr_of_players) + generate_age_I_manufactured_goods(nr_of_players) + generate_age_I_civilian_structures(nr_of_players) + generate_age_I_scientific_structures(nr_of_players) + generate_age_I_commerical_structures(nr_of_players) + generate_age_I_millitary_structures(nr_of_players)

def generate_age_I_raw_material_cards(nr_of_players): # should we add cost as 0 or let it be None?
    lumber_yard1 = RawMaterial(1, "Brown", "3+", "lumber_yard1", wood = 1)
    lumber_yard2 = RawMaterial(1, "Brown", "4+", "lumber_yard2", wood = 1)

    clay_pool1 = RawMaterial(1, "Brown", "3+", "clay_pool1", clay = 1)
    clay_pool2 = RawMaterial(1, "Brown", "5+", "clay_pool2", clay = 1)

    stone_pit1 = RawMaterial(1, "Brown", "3+", "stone_pit1", stone = 1)
    stone_pit2 = RawMaterial(1, "Brown", "5+", "stone_pit2", stone = 1)

    ore_vein1 = RawMaterial(1, "Brown", "3+", "stone_pit1", ore = 1)
    ore_vein2 = RawMaterial(1, "Brown", "4+", "stone_pit2", ore = 1)

    timber_yard1 = RawMaterial(1, "Brown", "3+", "timber_yard1", cost={"coins": 1}, resource_choices={"choices": [{"wood": 1, "ore": 1, "clay": 1, "stone": 1}]})

    forest_cave1 = RawMaterial(1, "Brown", "5+", "forest_cave1", cost={"coins":1}, resource_choices={"choices": [{"wood": 1, "ore": 1}]})

    excavation1 = RawMaterial(1, "Brown", "4+", "excavation1", cost={"coins": 1}, resource_choices={"choices": [{"stone": 1, "clay": 1}]})

    clay_pit1 = RawMaterial(1, "Brown", "3+", "clay_pit1", cost={"coins": 1}, resource_choices={"choices": [{"stone": 1, "clay": 1}]})

    mine1 = RawMaterial(1, "Brown", "6+", "mine1", cost={"coins": 1}, resource_choices={"choices": [{"stone": 1, "ore": 1}]})

    tree_farm1 = RawMaterial(1, "Brown", "6+", "tree_farm1", cost={"coins": 1}, resource_choices={"choices": [{"wood": 1, "clay": 1}]})

    three_players = [lumber_yard1, clay_pool1, stone_pit1, ore_vein1, timber_yard1, clay_pit1]
    four_players = [lumber_yard2, ore_vein2, excavation1]
    five_players = [clay_pool2, stone_pit2, forest_cave1]
    six_players = [mine1, tree_farm1]
    if nr_of_players == 3:
        return three_players
    elif nr_of_players == 4:
        return three_players + four_players
    elif nr_of_players == 5:
        return three_players + four_players + five_players
    elif nr_of_players >= 6 and nr_of_players <= 7:
        return three_players + four_players + five_players + six_players
    else:
        raise Exception("nr_of_players must be 3-7")

def generate_age_I_manufactured_goods(nr_of_players):
    glassworks1 = ManufacturedGood(1, "Grey", "3+", "glassworks1", glass = 1)
    glassworks2 = ManufacturedGood(1, "Grey", "6+", "glassworks2", glass = 1)
    press1 = ManufacturedGood(1, "Grey", "3+", "press1", papyrus = 1)
    press2 = ManufacturedGood(1, "Grey", "6+", "press2", papyrus = 1)
    loom1 = ManufacturedGood(1, "Grey", "3+", "loom1", cloth = 1)
    loom2 = ManufacturedGood(1, "Grey", "6+", "loom2", cloth = 1)

    three_players = [glassworks1, press1, loom1]
    six_players = [glassworks2, press2, loom2]

    if nr_of_players >= 3 and nr_of_players <= 5:
        return three_players
    elif nr_of_players >= 6 and nr_of_players <= 7:
        return three_players + six_players
    else:
        raise Exception("nr_of_players must be 3-7")

def generate_age_I_civilian_structures(nr_of_players):
    altar1 = CivilianStructure(1, "Blue", "3+", "altar1", victory_points=2, symbol=["Star"])
    altar2 = CivilianStructure(1, "Blue", "5+", "altar2", victory_points=2, symbol=["Star"])

    baths1 = CivilianStructure(1, "Blue", "3+", "baths1", victory_points=3, cost={"stone": 1}, symbol=["Waterdrop"])
    baths2 = CivilianStructure(1, "Blue", "7+", "baths2", victory_points=3, cost={"stone": 1}, symbol=["Waterdrop"])

    theater1 = CivilianStructure(1, "Blue", "3+", "theater1", victory_points=3, symbol=["Mask"])
    theater2 = CivilianStructure(1, "Blue", "6+", "theater2", victory_points=3, symbol=["Mask"])

    well1 = CivilianStructure(1, "Blue", "4+", "well1", victory_points=3, symbol=["Hammer"])
    well2 = CivilianStructure(1, "Blue", "7+", "well2", victory_points=3, symbol=["Hammer"])

    three_players = [altar1, baths1, theater1]
    four_players = [well1]
    five_players = [altar2]
    six_players = [theater2]
    seven_players = [baths2, well2]

    if nr_of_players == 3:
        return three_players
    elif nr_of_players == 4:
        return three_players + four_players
    elif nr_of_players == 5:
        return three_players + four_players + five_players
    elif nr_of_players == 6:
        return three_players + four_players + five_players + six_players
    elif nr_of_players == 7:
        return three_players + four_players + five_players + six_players + seven_players
    else:
        raise Exception("nr_of_players must be 3-7")

def generate_age_I_scientific_structures(nr_of_players):
    apothecary1 = ScientificStructure(1, "Green", "3+", "apothecary1", cost={"cloth":1}, compass=1, symbol=["Horseshoe", "Mortar"] )
    apothecary2 = ScientificStructure(1, "Green", "5+", "apothecary2", cost={"cloth":1}, compass=1, symbol=["Horseshoe", "Mortar"] )

    workshop1 = ScientificStructure(1, "Green", "3+", "workshop1", cost={"glass": 1}, gear=1, symbol=["Dart Board", "Genie Bottle"])
    workshop2 = ScientificStructure(1, "Green", "7+", "workshop2", cost={"glass": 1}, gear=1, symbol=["Dart Board", "Genie Bottle"])

    scriptorium1 = ScientificStructure(1, "Green", "3+", "scriptorium1", cost={"papyrus":1}, tablet=1, symbol=["Scale", "Book"])
    scriptorium2 = ScientificStructure(1, "Green", "4+", "scriptorium2", cost={"papyrus":1}, tablet=1, symbol=["Scale", "Book"])

    three_players = [apothecary1, workshop1, scriptorium1]
    four_players = [scriptorium2]
    five_players = [apothecary2]
    seven_players = [workshop2]
    if nr_of_players == 3:
        return three_players
    elif nr_of_players == 4:
        return three_players + four_players
    elif nr_of_players >= 5 and nr_of_players <= 6:
        return three_players + four_players + five_players
    elif nr_of_players == 7:
        return three_players + four_players + five_players + seven_players
    else:
        raise Exception("nr_of_players must be 3-7")

def generate_age_I_commerical_structures(nr_of_players):
    east_trading_post1 = CommercialStructure(1, "Yellow", "3+", "east_trading_post1", east_trading=True, symbol=["Table"])
    east_trading_post2 = CommercialStructure(1, "Yellow", "7+", "east_trading_post2", east_trading=True, symbol=["Table"])

    west_trading_post1 = CommercialStructure(1, "Yellow", "3+", "west_trading_post1", west_trading=True, symbol=["Table"])
    west_trading_post2 = CommercialStructure(1, "Yellow", "7+", "west_trading_post2", west_trading=True, symbol=["Table"])

    tavern1 = CommercialStructure(1, "Yellow", "4+", "tavern1", gold=5)
    tavern2 = CommercialStructure(1, "Yellow", "5+", "tavern2", gold=5)
    tavern3 = CommercialStructure(1, "Yellow", "7+", "tavern3", gold=5)

    marketplace1 = CommercialStructure(1, "Yellow", "3+", "marketplace1", marketplace=True, symbol=["Camel"])
    marketplace2 = CommercialStructure(1, "Yellow", "6+", "marketplace2", marketplace=True, symbol=["Camel"])

    three_players = [east_trading_post1, west_trading_post1, marketplace1]
    four_players = [tavern1]
    five_players = [tavern2]
    six_players = [marketplace2]
    seven_players = [east_trading_post2, west_trading_post2, tavern2]
    if nr_of_players == 3:
        return three_players 
    elif nr_of_players == 4:
        return three_players + four_players
    elif nr_of_players == 5:
        return three_players + four_players + five_players
    elif nr_of_players == 6:
        return three_players + four_players + five_players + six_players
    elif nr_of_players == 7:
        return three_players + four_players + five_players + six_players + seven_players
    else:
        raise Exception("nr_of_players is wrong, must be 3-7")
    

def generate_age_I_millitary_structures(nr_of_players):
    stockade1 = MilitaryStructure(1, "Red", "3+", "stockade1", cost={"wood": 1}, shield=1)
    stockade2 = MilitaryStructure(1, "Red", "7+", "stockade2", cost={"wood": 1}, shield=1)

    barracks1 = MilitaryStructure(1, "Red", "3+", "barracks1", cost={"ore": 1}, shield=1)
    barracks2 = MilitaryStructure(1, "Red", "5+", "barracks2", cost={"ore": 1}, shield=1)

    guard_tower1 = MilitaryStructure(1, "Red", "3+", "guard_tower1", cost={"clay": 1}, shield=1)
    guard_tower2 = MilitaryStructure(1, "Red", "4+", "guard_tower2", cost={"clay": 1}, shield=1)

    three_players = [stockade1, barracks1, guard_tower1]
    four_players = [guard_tower2]
    five_players = [barracks2]
    seven_players = [stockade2]
    if nr_of_players == 3:
        return three_players
    elif nr_of_players == 4:
        return three_players + four_players
    elif nr_of_players >= 5 and nr_of_players <= 6:
        return three_players + four_players + five_players
    elif nr_of_players == 7:
        return three_players + four_players + five_players + seven_players
    else:
        raise Exception("nr_of_players must be 3-7")