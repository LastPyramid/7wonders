from ..game.models import (
    RawMaterial, ManufacturedGood, CivilianStructure,
    ScientificStructure, CommercialStructure, MilitaryStructure, Guild
)

def generate_age_III_cards(nr_of_players):
    if nr_of_players < 3:
        print("too few players")
    else:
        return generate_age_III_civilian_structures(nr_of_players) + generate_age_III_scientific_structures(nr_of_players) + generate_age_III_commercial_structures(nr_of_players) + generate_age_III_military_structures(nr_of_players) + generate_age_III_guilds(nr_of_players)

def generate_age_III_civilian_structures(nr_of_players):
    pantheon1 = CivilianStructure(3, "Blue", "3+", "pantheon1", cost={"clay": 2, "stone":1, "papyrus": 1, "glass": 1, "cloth": 1, "symbol":"Star"}, victory_points=7)
    pantheon2 = CivilianStructure(3, "Blue", "6+", "pantheon2", cost={"clay": 2, "stone":1, "papyrus": 1, "glass": 1, "cloth": 1, "symbol":"Star"}, victory_points=7)

    gardens1 = CivilianStructure(3, "Blue", "3+", "gardens1", cost={"wood": 2, "clay": 1, "symbol":"Mask"}, victory_points=5)
    gardens2 = CivilianStructure(3, "Blue", "4+", "gardens2", cost={"wood": 2, "clay": 1, "symbol":"Mask"}, victory_points=5)

    town_hall1 = CivilianStructure(3, "Blue", "3+", "town_hall1", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)
    town_hall2 = CivilianStructure(3, "Blue", "6+", "town_hall2", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)

    palace1 = CivilianStructure(3, "Blue", "3+", "palace1", cost={"wood": 1, "clay": 1, "stone": 1, "ore": 1, "glass": 1, "cloth": 1, "papyrus": 1}, victory_points=8)
    palace2 = CivilianStructure(3, "Blue", "7+", "palace2", cost={"wood": 1, "clay": 1, "stone": 1, "ore": 1, "glass": 1, "cloth": 1, "papyrus": 1}, victory_points=8)

    senate1 = CivilianStructure(3, "Blue", "3+", "senate1", cost={"wood": 2, "ore": 1, "stone": 1, "symbol":"Temple"}, victory_points=6)
    senate2 = CivilianStructure(3, "Blue", "5+", "senate2", cost={"wood": 2, "ore": 1, "stone": 1, "symbol":"Temple"}, victory_points=6)

    three_players = [pantheon1, gardens1, town_hall1, palace1, senate1]
    four_players = [gardens2]
    five_players = [senate2]
    six_players = [pantheon2, town_hall2]
    seven_players = [palace2]
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
        raise Exception("nr_of_players should be 3-7")

def generate_age_III_scientific_structures(nr_of_players):
    lodge1 = ScientificStructure(3, "Green", "3+", "lodge1", cost={"clay": 2, "papyrus": 1, "cloth": 1, "symbol":"Torch"}, compass=1)
    lodge2 = ScientificStructure(3, "Green", "6+", "lodge2", cost={"clay": 2, "papyrus": 1, "cloth": 1, "symbol":"Torch"}, compass=1)

    observatory1 = ScientificStructure(3, "Green", "3+", "observatory1", cost={"ore": 2, "glass": 1, "cloth": 1, "symbol":"Planets"}, gear=1)
    observatory2 = ScientificStructure(3, "Green", "7+", "observatory2", cost={"ore": 2, "glass": 1, "cloth": 1, "symbol":"Planets"}, gear=1)

    university1 = ScientificStructure(3, "Green", "3+", "university1", cost={"wood": 2, "glass": 1, "papyrus": 1, "symbol":"Scroll"}, tablet=1)
    university2 = ScientificStructure(3, "Green", "4+", "university2", cost={"wood": 2, "glass": 1, "papyrus": 1, "symbol":"Scroll"}, tablet=1)

    academy1 = ScientificStructure(3, "Green", "3+", "academy1", cost={"stone": 3, "glass": 1, "symbol":"Lyre"}, compass=1)
    academy2 = ScientificStructure(3, "Green", "7+", "academy2", cost={"stone": 3, "glass": 1, "symbol":"Lyre"}, compass=1)

    study1 = ScientificStructure(3, "Green", "3+", "study1", cost={"wood": 1, "papyrus": 1, "cloth": 1, "symbol":"Feather"}, gear=1)
    study2 = ScientificStructure(3, "Green", "5+", "study2", cost={"wood": 1, "papyrus": 1, "cloth": 1, "symbol":"Feather"}, gear=1)

    three_players = [lodge1, observatory1, university1, academy1, study1]
    four_players = [university2]
    five_players = [study2]
    six_players = [lodge2]
    seven_players = [observatory2, academy2]
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
        raise Exception("nr_of_players should be 3-7")

def generate_age_III_commercial_structures(nr_of_players):
    haven1 = CommercialStructure(3, "Yellow", "3+", "haven1", cost={"wood": 1, "ore": 1, "cloth": 1, "symbol":"Barrel"},
            gain={"gain": {"coins": 1, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Brown"}})
    haven2 = CommercialStructure(3, "Yellow", "4+", "haven2", cost={"wood": 1, "ore": 1, "cloth": 1, "symbol":"Barrel"},
            gain={"gain": {"coins": 1, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Brown"}})

    lighthouse1 = CommercialStructure(3, "Yellow", "3+", "lighthouse1", cost={"stone": 1, "glass": 1, "symbol":"Lighthouse"},
            gain={"gain": {"coins": 1, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Yellow"}})
    lighthouse2 = CommercialStructure(3, "Yellow", "6+", "lighthouse2", cost={"stone": 1, "glass": 1, "symbol":"Lighthouse"},
            gain={"gain": {"coins": 1, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Yellow"}})

    chamber_of_commerce1 = CommercialStructure(3, "Yellow", "4+", "chamber_of_commerce1", cost={"clay": 2, "papyrus": 1},
            gain={"gain": {"coins": 2, "victory_point": 2}, "condition": {"location": ["self"], "activity": "Gray"}})
    chamber_of_commerce2 = CommercialStructure(3, "Yellow", "6+", "chamber_of_commerce2", cost={"clay": 2, "papyrus": 1},
            gain={"gain": {"coins": 2, "victory_point": 2}, "condition": {"location": ["self"], "activity": "Gray"}})

    arena1 = CommercialStructure(3, "Yellow", "3+", "arena1", cost={"stone": 2, "ore": 1, "symbol":"Lightning Bolt"},
            gain={"gain": {"coins": 3, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Stage of Wonders"}})
    arena2 = CommercialStructure(3, "Yellow", "5+", "arena2", cost={"stone": 2, "ore": 1, "symbol":"Lightning Bolt"},
            gain={"gain": {"coins": 3, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Stage of Wonders"}})

    ludus1 = CommercialStructure(3, "Yellow", "5+", "ludus1", cost={"stone": 1, "ore": 1},
            gain={"gain": {"coins": 3, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Red"}})
    ludus2 = CommercialStructure(3, "Yellow", "7+", "ludus2", cost={"stone": 2, "ore": 1},
            gain={"gain": {"coins": 3, "victory_point": 1}, "condition": {"location": ["self"], "activity": "Red"}})

    three_players = [haven1, lighthouse1, arena1]
    four_players = [haven2, chamber_of_commerce1]
    five_players = [arena2, ludus1]
    six_players = [lighthouse2, chamber_of_commerce2]
    seven_players = [ludus2]
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
        raise Exception("nr_of_players should be 3-7")

def generate_age_III_military_structures(nr_of_players):
    fortifications1 = MilitaryStructure(3, "Red", "3+", "fortifications1", cost={"stone": 3, "clay": 1, "symbol":"Wall"}, millitary_strength=3)
    fortifications2 = MilitaryStructure(3, "Red", "7+", "fortifications2", cost={"stone": 3, "clay": 1, "symbol":"Wall"}, millitary_strength=3)

    circus1 = MilitaryStructure(3, "Red", "4+", "circus1", cost={"clay": 3, "ore": 1, "symbol":"Helmet"}, millitary_strength=3)
    circus2 = MilitaryStructure(3, "Red", "6+", "circus2", cost={"clay": 3, "ore": 1, "symbol":"Helmet"}, millitary_strength=3)

    arsenal1 = MilitaryStructure(3, "Red", "3+", "arsenal1", cost={"wood": 2, "ore": 1, "cloth": 1}, millitary_strength=3)
    arsenal2 = MilitaryStructure(3, "Red", "5+", "arsenal2", cost={"wood": 2, "ore": 1, "cloth": 1}, millitary_strength=3)

    siege_workshop1 = MilitaryStructure(3, "Red", "3+", "siege_workshop1", cost={"clay": 3, "wood": 1, "symbol":"Saw"}, millitary_strength=3)
    siege_workshop2 = MilitaryStructure(3, "Red", "5+", "siege_workshop2", cost={"clay": 3, "wood": 1, "symbol":"Saw"}, millitary_strength=3)

    castrum1 = MilitaryStructure(3, "Red", "4+", "castrum1", cost={"clay": 3, "wood": 1, "papyrus":1}, millitary_strength=3)
    castrum2 = MilitaryStructure(3, "Red", "7+", "castrum2", cost={"clay": 3, "wood": 1, "papyrus":1}, millitary_strength=3)

    three_players = [fortifications1, arsenal1, siege_workshop1]
    four_players = [circus1, castrum1]
    five_players = [arsenal2, siege_workshop2]
    six_players = [circus2]
    seven_players = [fortifications2, castrum2]
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
        raise Exception("nr_of_players should be 3-7")

def generate_age_III_guilds(nr_of_players):
    workers_guild = Guild(3, "Purple", "3+", "workers_guild1", cost={"ore": 2, "wood":1, "stone": 1, "clay": 1}, location=["left", "right"], victory_points=1, activity=["Brown"])
    craftmens_guild = Guild(3, "Purple", "3+", "craftsmens_guild1", cost={"stone": 2, "ore": 2}, location=["left", "right"], victory_points=2, activity=["Gray"])
    traders_guild = Guild(3, "Purple", "3+", "traders_guild1", cost={"cloth": 1, "papyrus": 1, "glass": 1}, location=["left", "right"], victory_points=1, activity=["Yellow"])
    philosophers_guild = Guild(3, "Purple", "3+", "philosophers_guild1", cost={"clay": 3, "papyrus": 1, "cloth":1}, location=["left", "right"], victory_points=1, activity=["Green"])
    spies_guild = Guild(3, "Purple", "3+", "spies_guild1", cost={"clay": 2, "glass":1}, location=["left", "right"], victory_points=1, activity=["Red"])
    shipowners_guild = Guild(3, "Purple", "3+", "shipowners_guild1", cost={"wood": 3, "glass":1, "papyrus": 1}, location=["self"], victory_points=1, activity=["Brown", "Gray", "Purple"])
    scientists_guild = Guild(3, "Purple", "3+", "scientists_guild1", cost={"wood": 2, "ore": 2, "papyrus":1}, resource_choices={"choices": [{"compass": 1, "tablet": 1, "gear": 1}]})
    magistrates_guild = Guild(3, "Purple", "3+", "magistrates_guild1", cost={"wood": 3, "stone":1, "cloth": 1}, location=["left", "right"], victory_points=1, activity=["Blue"])
    builders_guild = Guild(3, "Purple", "3+", "builders_guild1", cost={"stone": 3, "clay": 2, "glass": 1}, location=["self", "left", "right"], victory_points=1, activity=["Wonders"])
    decorators_guild = Guild(3, "Purple", "3+", "decorators_guild1", cost={"ore": 2, "stone": 1, "cloth":1}, victory_points=7)

    if nr_of_players >= 3 and nr_of_players <= 7:
        return [workers_guild, craftmens_guild, traders_guild, philosophers_guild, spies_guild, decorators_guild, shipowners_guild, scientists_guild, magistrates_guild, builders_guild]
    else:
        raise Exception("nr_of_players should be 3-7")