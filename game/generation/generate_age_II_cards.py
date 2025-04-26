from ..game.models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure
def generate_age_II_cards(nr_of_players):
    if nr_of_players < 3:
        print("too few players")
    else:
        return generate_age_II_raw_material_cards(nr_of_players) + generate_age_II_manufactured_goods(nr_of_players) + generate_age_II_civilian_structures(nr_of_players) + generate_age_II_scientific_structures(nr_of_players) + generate_age_II_commercial_structures(nr_of_players) + generate_age_II_military_structures(nr_of_players)

def generate_age_II_raw_material_cards(nr_of_players):
    saw_mill1 = RawMaterial(2, "Brown", "3+", "sawmill1", cost={"coins": 1}, wood=2)
    saw_mill2 = RawMaterial(2, "Brown", "4+", "sawmill2", cost={"coins": 1}, wood=2)

    brickyard1 = RawMaterial(2, "Brown", "3+", "brickyard1", cost={"coins": 1}, clay=2)
    brickyard2 = RawMaterial(2, "Brown", "4+", "brickyard2", cost={"coins": 1}, clay=2)

    quarry1 = RawMaterial(2, "Brown", "3+", "quarry1", cost={"coins": 1}, stone=2)
    quarry2 = RawMaterial(2, "Brown", "4+", "quarry2", cost={"coins": 1}, stone=2)

    foundry1 = RawMaterial(2, "Brown", "3+", "foundry1", cost={"coins": 1}, ore=2)
    foundry2 = RawMaterial(2, "Brown", "4+", "foundry2", cost={"coins": 1}, ore=2)
    
    three_players = [saw_mill1, brickyard1, quarry1, foundry1]
    four_players = [saw_mill2, brickyard2, quarry2, foundry2]
    if nr_of_players == 3:
        return three_players
    elif nr_of_players >= 3 and nr_of_players <= 7:
        return three_players + four_players
    else:
        raise Exception("nr_of_players should me 3-7")


def generate_age_II_manufactured_goods(nr_of_players):
    glassworks1 = ManufacturedGood(2, "Gray", "3+", "glassworks1", glass=1)
    glassworks2 = ManufacturedGood(2, "Gray", "5+", "glassworks2", glass=1)

    press1 = ManufacturedGood(2, "Gray", "3+", "press1", papyrus=1)
    press2 = ManufacturedGood(2, "Gray", "5+", "press2", papyrus=1)

    loom1 = ManufacturedGood(2, "Gray", "3+", "loom1", cloth=1)
    loom2 = ManufacturedGood(2, "Gray", "5+", "loom2", cloth=1)
    
    three_players = [glassworks1, press1, loom1]
    five_players = [glassworks2, press2, loom2]
    if nr_of_players >= 3 and nr_of_players <= 4:
        return three_players
    elif nr_of_players >= 5 and nr_of_players <= 7:
        return three_players + five_players
    else:
        raise Exception("nr_of_players should me 3-7")

def generate_age_II_civilian_structures(nr_of_players):
    aqueduct1 = CivilianStructure(2, "Blue", "3+", "aqueduct1", cost={"stone": 3, "symbol": "Waterdrop"}, victory_points=5)
    aqueduct2 = CivilianStructure(2, "Blue", "7+", "aqueduct2", cost={"stone": 3, "symbol": "Waterdrop"}, victory_points=5)

    temple1 = CivilianStructure(2, "Blue", "3+", "temple1", cost={"wood": 1, "clay": 1, "glass": 1}, victory_points=4)
    temple2 = CivilianStructure(2, "Blue", "6+", "temple2", cost={"wood": 1, "clay": 1, "glass": 1}, victory_points=4)

    statue1 = CivilianStructure(2, "Blue", "3+", "statue1", cost={"ore": 2, "wood": 1, "symbol": "Hammer"}, victory_points=4)
    statue2 = CivilianStructure(2, "Blue", "7+", "statue2", cost={"ore": 2, "wood": 1, "symbol": "Hammer"}, victory_points=4)

    courthouse1 = CivilianStructure(2, "Blue", "3+", "courthouse1", cost={"clay": 2, "cloth": 1, "symbol":"Scale"}, victory_points=4)
    courthouse2 = CivilianStructure(2, "Blue", "5+", "courthouse2", cost={"clay": 2, "cloth": 1, "symbol":"Scale"}, victory_points=4)

    three_players = [aqueduct1, temple1, statue1, courthouse1]
    five_players = [courthouse2]
    six_players = [temple2]
    seven_players = [aqueduct2, statue2]
    if nr_of_players >= 3 and nr_of_players <= 4:
        return three_players
    elif nr_of_players == 5:
        return three_players + five_players
    elif nr_of_players == 6:
        return three_players + five_players + six_players
    elif nr_of_players == 7:
        return three_players + five_players + six_players + seven_players
    else:
        raise Exception("nr_of_players should me 3-7")

def generate_age_II_scientific_structures(nr_of_players):
    library1 = ScientificStructure(2, "Green", "3+", "library1", cost={"stone": 2, "cloth": 1, "symbol":"Book"}, tablet=1, symbol=["Temple", "Scroll"])
    library2 = ScientificStructure(2, "Green", "6+", "library2", cost={"stone": 2, "cloth": 1, "symbol":"Book"}, tablet=1, symbol=["Temple", "Scroll"])

    dispensary1 = ScientificStructure(2, "Green", "3+", "dispensary1", cost={"ore": 2, "glass": 1, "symbol":"Mortar"}, compass=1, symbol=["Lightning Bolt", "Torch"])
    dispensary2 = ScientificStructure(2, "Green", "4+", "dispensary2", cost={"ore": 2, "glass": 1, "symbol":"Mortar"}, compass=1, symbol=["Lightning Bolt", "Torch"])

    school1 = ScientificStructure(2, "Green", "3+", "school1", cost={"wood": 1, "papyrus": 1}, tablet=1, symbol=["Lyre", "Feather"])
    school2 = ScientificStructure(2, "Green", "7+", "school2", cost={"wood": 1, "papyrus": 1}, tablet=1, symbol=["Lyre", "Feather"])

    laboratory1 = ScientificStructure(2, "Green", "3+", "laboratory1", cost={"clay": 2, "papyrus": 1, "symbol":"Genie Bottle"}, gear=1, symbol=["Planets", "Saw"])
    laboratory2 = ScientificStructure(2, "Green", "5+", "laboratory2", cost={"clay": 2, "papyrus": 1, "symbol":"Genie Bottle"}, gear=1, symbol=["Planets", "Saw"])

    three_players = [library1, dispensary1, school1, laboratory1]
    four_players = [dispensary2]
    five_players = [laboratory2]
    six_players = [library2]
    seven_players = [school2]
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
        raise Exception("nr_of_players should me 3-7")

def generate_age_II_commercial_structures(nr_of_players):
    caravansery1 = CommercialStructure(2, "Yellow", "3+", "caravansery1", cost={"wood": 2, "symbol":"Camel"}, resource_choices={"choices": [{"wood": 1, "ore": 1, "clay": 1, "stone": 1}]}, symbol="Lighthouse")
    caravansery2 = CommercialStructure(2, "Yellow", "5+", "caravansery2", cost={"wood": 2, "symbol":"Camel"}, resource_choices={"choices": [{"wood": 1, "ore": 1, "clay": 1, "stone": 1}]}, symbol="Lighthouse")
    caravansery3 = CommercialStructure(2, "Yellow", "6+", "caravansery3", cost={"wood": 2, "symbol":"Camel"}, resource_choices={"choices": [{"wood": 1, "ore": 1, "clay": 1, "stone": 1}]}, symbol="Lighthouse")

    forum1 = CommercialStructure(2, "Yellow", "3+", "forum1", cost={"clay": 2, "symbol":"Table"}, resource_choices={"choices": [{"glass": 1, "papyrus": 1, "cloth": 1}]}, symbol=["Barrel"])
    forum2 = CommercialStructure(2, "Yellow", "6+", "forum2", cost={"clay": 2, "symbol":"Table"}, resource_choices={"choices": [{"glass": 1, "papyrus": 1, "cloth": 1}]}, symbol=["Barrel"])
    forum3 = CommercialStructure(2, "Yellow", "7+", "forum3", cost={"clay": 2, "symbol":"Table"}, resource_choices={"choices": [{"glass": 1, "papyrus": 1, "cloth": 1}]}, symbol=["Barrel"])

    vineyard1 = CommercialStructure(2, "Yellow", "3+", "vineyard1", gain={"gain": {"coins": 1}, "location": ["left", "right", "self"], "activity": "Brown"})
    vineyard2 = CommercialStructure(2, "Yellow", "6+", "vineyard2", gain={"gain": {"coins": 1}, "location": ["left", "right", "self"], "activity": "Brown"})

    bazaar1 = CommercialStructure(2, "Yellow", "4+", "bazaar1", gain={"gain": {"coins": 2}, "location": ["left", "right", "self"], "activity": "Yellow"})
    bazaar2 = CommercialStructure(2, "Yellow", "7+", "bazaar2", gain={"gain": {"coins": 2}, "location": ["left", "right", "self"], "activity": "Yellow"})

    three_players = [caravansery1, forum1, vineyard1]
    four_players = [bazaar1]
    five_players = [caravansery2]
    six_players = [caravansery3, forum2, vineyard2]
    seven_players = [forum3, bazaar2]
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
        raise Exception("nr_of_players should me 3-7")


def generate_age_II_military_structures(nr_of_players):
    walls1 = MilitaryStructure(2, "Red", "3+", "walls1", cost={"stone": 3}, millitary_strength=2, symbol=["Wall"])
    walls2 = MilitaryStructure(2, "Red", "7+", "walls2", cost={"stone": 3}, millitary_strength=2, symbol=["Wall"])

    training_grounds1 = MilitaryStructure(2, "Red", "4+", "training_ground1", cost={"wood": 1, "ore": 2}, millitary_strength=2, symbol=["Helmet"])
    training_grounds2 = MilitaryStructure(2, "Red", "6+", "training_ground2", cost={"wood": 1, "ore": 2}, millitary_strength=2, symbol=["Helmet"])
    training_grounds3 = MilitaryStructure(2, "Red", "7+", "training_ground3", cost={"wood": 1, "ore": 2}, millitary_strength=2, symbol=["Helmet"])

    stables1 = MilitaryStructure(2, "Red", "3+", "stables1", cost={"wood": 1, "ore": 1, "clay": 1, "symbol":"Horseshoe"}, millitary_strength=2)
    stables2 = MilitaryStructure(2, "Red", "5+", "stables2", cost={"wood": 1, "ore": 1, "clay": 1, "symbol":"Horseshoe"}, millitary_strength=2)

    archery_range1 = MilitaryStructure(2, "Red", "3+", "archery_range1", cost={"wood": 2, "ore": 1, "symbol":"Dart Board"}, millitary_strength=2)
    archery_range2 = MilitaryStructure(2, "Red", "6+", "archery_range2", cost={"wood": 2, "ore": 1, "symbol":"Dart Board"}, millitary_strength=2)

    three_players = [walls1, stables1, archery_range1]
    four_players = [training_grounds1]
    five_players = [stables2]
    six_players = [training_grounds2, archery_range2]
    seven_players = [walls2, training_grounds3]
    if nr_of_players == 3:
        return three_players
    if nr_of_players == 4:
        return three_players + four_players
    if nr_of_players == 5:
        return three_players + four_players + five_players
    if nr_of_players == 6:
        return three_players + four_players + five_players + six_players
    if nr_of_players == 7:
        return three_players + four_players + five_players + six_players + seven_players
    else:
        raise Exception("nr_of_players should me 3-7")
