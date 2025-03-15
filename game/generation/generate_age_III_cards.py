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
    pantheon1 = CivilianStructure(3, "Blue", "3+", "Pantheon", cost={"clay": 2, "stone":1, "papyrus": 1, "glass": 1, "cloth": 1, "symbol":"Star"}, victory_points=7)
    pantheon2 = CivilianStructure(3, "Blue", "6+", "Pantheon", cost={"clay": 2, "stone":1, "papyrus": 1, "glass": 1, "cloth": 1, "symbol":"Star"}, victory_points=7)

    gardens1 = CivilianStructure(3, "Blue", "3+", "Gardens", cost={"wood": 2, "clay": 1, "symbol":"Mask"}, victory_points=5)
    gardens2 = CivilianStructure(3, "Blue", "4+", "Gardens", cost={"wood": 2, "clay": 1, "symbol":"Mask"}, victory_points=5)

    town_hall1 = CivilianStructure(3, "Blue", "3+", "Town Hall", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)
    town_hall2 = CivilianStructure(3, "Blue", "6+", "Town Hall", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)

    palace1 = CivilianStructure(3, "Blue", "3+", "Palace", cost={"wood": 1, "clay": 1, "stone": 1, "ore": 1, "glass": 1, "cloth": 1, "papyrus": 1}, victory_points=8)
    palace2 = CivilianStructure(3, "Blue", "7+", "Palace", cost={"wood": 1, "clay": 1, "stone": 1, "ore": 1, "glass": 1, "cloth": 1, "papyrus": 1}, victory_points=8)

    senate1 = CivilianStructure(3, "Blue", "3+", "Senate", cost={"wood": 2, "ore": 1, "stone": 1, "symbol":"Temple"}, victory_points=6)
    senate2 = CivilianStructure(3, "Blue", "5+", "Senate", cost={"wood": 2, "ore": 1, "stone": 1, "symbol":"Temple"}, victory_points=6)

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
    lodge1 = ScientificStructure(3, "Green", "3+", "Lodge", cost={"clay": 2, "papyrus": 1, "cloth": 1, "symbol":"Torch"}, compass=1)
    lodge2 = ScientificStructure(3, "Green", "6+", "Lodge", cost={"clay": 2, "papyrus": 1, "cloth": 1, "symbol":"Torch"}, compass=1)

    observatory1 = ScientificStructure(3, "Green", "3+", "Observatory", cost={"ore": 2, "glass": 1, "cloth": 1, "symbol":"Planets"}, gear=1)
    observatory2 = ScientificStructure(3, "Green", "7+", "Observatory", cost={"ore": 2, "glass": 1, "cloth": 1, "symbol":"Planets"}, gear=1)

    university1 = ScientificStructure(3, "Green", "3+", "University", cost={"wood": 2, "glass": 1, "papyrus": 1, "symbol":"Scroll"}, tablet=1)
    university2 = ScientificStructure(3, "Green", "4+", "University", cost={"wood": 2, "glass": 1, "papyrus": 1, "symbol":"Scroll"}, tablet=1)

    academy1 = ScientificStructure(3, "Green", "3+", "Academy", cost={"stone": 3, "glass": 1, "symbol":"Lyre"}, compass=1)
    academy2 = ScientificStructure(3, "Green", "7+", "Academy", cost={"stone": 3, "glass": 1, "symbol":"Lyre"}, compass=1)

    study1 = ScientificStructure(3, "Green", "3+", "Study", cost={"wood": 1, "papyrus": 1, "cloth": 1, "symbol":"Feather"}, gear=1)
    study2 = ScientificStructure(3, "Green", "5+", "Study", cost={"wood": 1, "papyrus": 1, "cloth": 1, "symbol":"Feather"}, gear=1)

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
    haven1 = CommercialStructure(3, "Yellow", "3+", "Haven", cost={"wood": 1, "ore": 1, "cloth": 1, "symbol":"Barrel"},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Brown"}})
    haven2 = CommercialStructure(3, "Yellow", "4+", "Haven", cost={"wood": 1, "ore": 1, "cloth": 1, "symbol":"Barrel"},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Brown"}})

    lighthouse1 = CommercialStructure(3, "Yellow", "3+", "Lighthouse", cost={"stone": 1, "glass": 1, "symbol":"Lighthouse"},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Yellow"}})
    lighthouse2 = CommercialStructure(3, "Yellow", "6+", "Lighthouse", cost={"stone": 1, "glass": 1, "symbol":"Lighthouse"},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Yellow"}})

    chamber_of_commerce1 = CommercialStructure(3, "Yellow", "4+", "Chamber Of Commerce", cost={"clay": 2, "papyrus": 1},
            resource_choices={"choices": [{"coin": 2}, {"victory_point": 2}], "condition": {"location": ["self"], "activity": "Gray"}})
    chamber_of_commerce2 = CommercialStructure(3, "Yellow", "6+", "Chamber Of Commerce", cost={"clay": 2, "papyrus": 1},
            resource_choices={"choices": [{"coin": 2}, {"victory_point": 2}], "condition": {"location": ["self"], "activity": "Gray"}})

    arena1 = CommercialStructure(3, "Yellow", "3+", "Arena", cost={"stone": 2, "ore": 1, "symbol":"Lightning Bolt"},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Stage of Wonders"}})
    arena2 = CommercialStructure(3, "Yellow", "5+", "Arena", cost={"stone": 2, "ore": 1, "symbol":"Lightning Bolt"},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Stage of Wonders"}})

    ludus1 = CommercialStructure(3, "Yellow", "5+", "Ludus", cost={"stone": 1, "ore": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Red"}})
    ludus2 = CommercialStructure(3, "Yellow", "7+", "Ludus", cost={"stone": 2, "ore": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Red"}})

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
    fortifications1 = MilitaryStructure(3, "Red", "3+", "Fortifications", cost={"stone": 3, "clay": 1, "symbol":"Wall"}, shield=3)
    fortifications2 = MilitaryStructure(3, "Red", "7+", "Fortifications", cost={"stone": 3, "clay": 1, "symbol":"Wall"}, shield=3)

    circus1 = MilitaryStructure(3, "Red", "4+", "Circus", cost={"clay": 3, "ore": 1, "symbol":"Helmet"}, shield=3)
    circus2 = MilitaryStructure(3, "Red", "6+", "Circus", cost={"clay": 3, "ore": 1, "symbol":"Helmet"}, shield=3)

    arsenal1 = MilitaryStructure(3, "Red", "3+", "Arsenal", cost={"wood": 2, "ore": 1, "cloth": 1}, shield=3)
    arsenal2 = MilitaryStructure(3, "Red", "5+", "Arsenal", cost={"wood": 2, "ore": 1, "cloth": 1}, shield=3)

    siege_workshop1 = MilitaryStructure(3, "Red", "3+", "Siege Workshop", cost={"clay": 3, "wood": 1, "symbol":"Saw"}, shield=3)
    siege_workshop2 = MilitaryStructure(3, "Red", "5+", "Siege Workshop", cost={"clay": 3, "wood": 1, "symbol":"Saw"}, shield=3)

    castrum1 = MilitaryStructure(3, "Red", "4+", "Castrum", cost={"clay": 3, "wood": 1, "papyrus":1}, shield=3)
    castrum2 = MilitaryStructure(3, "Red", "7+", "Castrum", cost={"clay": 3, "wood": 1, "papyrus":1}, shield=3)

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
    workers_guild = Guild(3, "Purple", "3+", "Workers Guild", cost={"ore": 2, "wood":1, "stone": 1, "clay": 1}, location=["left", "right"], victory_points=1, activity=["Brown"])
    craftmens_guild = Guild(3, "Purple", "3+", "Craftmens Guild", cost={"stone": 2, "ore": 2}, location=["left", "right"], victory_points=2, activity=["Gray"])
    traders_guild = Guild(3, "Purple", "3+", "Traders Guild", cost={"cloth": 1, "papyrus": 1, "glass": 1}, location=["left", "right"], victory_points=1, activity=["Yellow"])
    philosophers_guild = Guild(3, "Purple", "3+", "Philosophers Guild", cost={"clay": 3, "papyrus": 1, "cloth":1}, location=["left", "right"], victory_points=1, activity=["Green"])
    spies_guild = Guild(3, "Purple", "3+", "Spies Guild", cost={"clay": 2, "glass":1}, location=["left", "right"], victory_points=1, activity=["Red"])
    shipowners_guild = Guild(3, "Purple", "3+", "Shipowners Guild", cost={"wood": 3, "glass":1, "papyrus": 1}, location=["self"], victory_points=1, activity=["Brown", "Gray", "Purple"])
    scientists_guild = Guild(3, "Purple", "3+", "Scientists Guild", cost={"wood": 2, "ore": 2, "papyrus":1}, resource_choices={"choices": [{"compass": 1, "tablet": 1, "gear": 1}]})
    magistrates_guild = Guild(3, "Purple", "3+", "Magistrates Guild", cost={"wood": 3, "stone":1, "cloth": 1}, location=["left", "right"], victory_points=1, activity=["Blue"])
    builders_guild = Guild(3, "Purple", "3+", "Builders Guild", cost={"stone": 3, "clay": 2, "glass": 1}, location=["self", "left", "right"], victory_points=1, activity=["Wonders"])
    decorators_guild = Guild(3, "Purple", "3+", "Decorators Guild", cost={"ore": 2, "stone": 1, "cloth":1}, victory_points=7)

    if nr_of_players >= 3 and nr_of_players <= 7:
        return [workers_guild, craftmens_guild, traders_guild, philosophers_guild, spies_guild, decorators_guild, shipowners_guild, scientists_guild, magistrates_guild, builders_guild]
    else:
        raise Exception("nr_of_players should be 3-7")