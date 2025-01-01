from ..game.models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure, Guild

def generate_age_III_cards(nr_of_players):
    if nr_of_players < 3:
        print("too few players")
    else:
        return generate_age_III_civilian_structures(nr_of_players) + generate_age_III_scientific_structures(nr_of_players) + generate_age_III_commercial_structures(nr_of_players) + generate_age_III_military_structures(nr_of_players) + generate_age_III_guilds(nr_of_players)

def generate_age_III_civilian_structures(nr_of_players):
    pantheon1 = CivilianStructure(3, "Blue", "4+", "Pantheon", cost={"clay": 2, "papyrus": 1, "glass": 1, "cloth": 1}, victory_points=7)
    pantheon2 = CivilianStructure(3, "Blue", "4+", "Pantheon", cost={"clay": 2, "papyrus": 1, "glass": 1, "cloth": 1}, victory_points=7)

    gardens1 = CivilianStructure(3, "Blue", "3+", "Gardens", cost={"wood": 2, "clay": 1}, victory_points=5)
    gardens2 = CivilianStructure(3, "Blue", "3+", "Gardens", cost={"wood": 2, "clay": 1}, victory_points=5)

    town_hall1 = CivilianStructure(3, "Blue", "3+", "Town Hall", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)
    town_hall2 = CivilianStructure(3, "Blue", "3+", "Town Hall", cost={"stone": 2, "ore": 1, "glass": 1}, victory_points=6)

    palace1 = CivilianStructure(3, "Blue", "5+", "Palace", cost={"wood": 1, "clay": 1, "stone": 1, "ore": 1, "glass": 1, "cloth": 1, "papyrus": 1}, victory_points=8)

    senate1 = CivilianStructure(3, "Blue", "3+", "Senate", cost={"wood": 2, "ore": 1, "stone": 1}, victory_points=6)
    senate2 = CivilianStructure(3, "Blue", "3+", "Senate", cost={"wood": 2, "ore": 1, "stone": 1}, victory_points=6)

    if nr_of_players == 5:
        return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2] + [pantheon1, pantheon2] + [palace1]
    elif nr_of_players == 4:
        return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2] + [pantheon1, pantheon2]
    return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2]

def generate_age_III_scientific_structures(nr_of_players):
    lodge1 = ScientificStructure(3, "Green", "3+", "Lodge", cost={"clay": 2, "papyrus": 1, "cloth": 1}, compass=1)
    lodge2 = ScientificStructure(3, "Green", "3+", "Lodge", cost={"clay": 2, "papyrus": 1, "cloth": 1}, compass=1)

    observatory1 = ScientificStructure(3, "Green", "4+", "Observatory", cost={"ore": 2, "glass": 1, "cloth": 1}, gear=1)
    observatory2 = ScientificStructure(3, "Green", "4+", "Observatory", cost={"ore": 2, "glass": 1, "cloth": 1}, gear=1)

    university1 = ScientificStructure(3, "Green", "3+", "University", cost={"wood": 2, "glass": 1, "papyrus": 1}, tablet=1)
    university2 = ScientificStructure(3, "Green", "3+", "University", cost={"wood": 2, "glass": 1, "papyrus": 1}, tablet=1)

    academy1 = ScientificStructure(3, "Green", "4+", "Academy", cost={"stone": 3, "glass": 1}, compass=1)
    academy2 = ScientificStructure(3, "Green", "4+", "Academy", cost={"stone": 3, "glass": 1}, compass=1)

    study1 = ScientificStructure(3, "Green", "3+", "Study", cost={"wood": 1, "papyrus": 1, "cloth": 1}, gear=1)
    study2 = ScientificStructure(3, "Green", "3+", "Study", cost={"wood": 1, "papyrus": 1, "cloth": 1}, gear=1)

    if nr_of_players >= 4:
        return [lodge1, lodge2, university1, university2, study1, study2] + [observatory1, observatory2, academy1, academy2]
    return [lodge1, lodge2, university1, university2, study1, study2]

def generate_age_III_commercial_structures(nr_of_players):
    haven1 = CommercialStructure(3, "Yellow", "3+", "Haven", cost={"wood": 1, "ore": 1, "cloth": 1},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Brown"}})
    haven2 = CommercialStructure(3, "Yellow", "3+", "Haven", cost={"wood": 1, "ore": 1, "cloth": 1},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Brown"}})

    lighthouse1 = CommercialStructure(3, "Yellow", "3+", "Lighthouse", cost={"stone": 1, "glass": 1},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Yellow"}})
    lighthouse2 = CommercialStructure(3, "Yellow", "3+", "Lighthouse", cost={"stone": 1, "glass": 1},
            resource_choices={"choices": [{"coin": 1}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Yellow"}})

    chamber_of_commerce1 = CommercialStructure(3, "Yellow", "4+", "Chamber Of Commerce", cost={"clay": 2, "papyrus": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 2}], "condition": {"location": ["self"], "activity": "Gray"}})
    chamber_of_commerce2 = CommercialStructure(3, "Yellow", "4+", "Chamber Of Commerce", cost={"clay": 2, "papyrus": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 2}], "condition": {"location": ["self"], "activity": "Gray"}})

    arena1 = CommercialStructure(3, "Yellow", "3+", "Arena", cost={"stone": 2, "ore": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Stage of Wonders"}})
    arena2 = CommercialStructure(3, "Yellow", "3+", "Arena", cost={"stone": 2, "ore": 1},
            resource_choices={"choices": [{"coin": 3}, {"victory_point": 1}], "condition": {"location": ["self"], "activity": "Stage of Wonders"}})

    if nr_of_players >= 4:
        return [haven1, haven2, lighthouse1, lighthouse2, arena1, arena2] + [chamber_of_commerce1, chamber_of_commerce2]
    return [haven1, haven2, lighthouse1, lighthouse2, arena1, arena2]

def generate_age_III_military_structures(nr_of_players):
    fortifications1 = MilitaryStructure(3, "Red", "3+", "Fortifications", cost={"stone": 3, "ore": 1}, shield=3)
    fortifications2 = MilitaryStructure(3, "Red", "3+", "Fortifications", cost={"stone": 3, "ore": 1}, shield=3)

    circus1 = MilitaryStructure(3, "Red", "4+", "Circus", cost={"clay": 3, "ore": 1}, shield=3)
    circus2 = MilitaryStructure(3, "Red", "4+", "Circus", cost={"clay": 3, "ore": 1}, shield=3)

    arsenal1 = MilitaryStructure(3, "Red", "4+", "Arsenal", cost={"wood": 2, "ore": 1, "cloth": 1}, shield=2)
    arsenal2 = MilitaryStructure(3, "Red", "4+", "Arsenal", cost={"wood": 2, "ore": 1, "cloth": 1}, shield=2)

    siege_workshop1 = MilitaryStructure(3, "Red", "3+", "Siege Workshop", cost={"wood": 3, "clay": 1}, shield=2)
    siege_workshop2 = MilitaryStructure(3, "Red", "3+", "Siege Workshop", cost={"wood": 3, "clay": 1}, shield=2)

    if nr_of_players >= 4:
        return [fortifications1, fortifications2, siege_workshop1, siege_workshop2] + [circus1, circus2, arsenal1, arsenal2]
    return [fortifications1, fortifications2, siege_workshop1, siege_workshop2]

def generate_age_III_guilds(nr_of_players):
    workers_guild = Guild(3, "Purple", "4+", "Workers Guild", cost={"ore": 2, "clay": 1}, location=["left", "right"], victory_points=1, activity=["Brown"])
    craftmens_guild = Guild(3, "Purple", "4+", "Craftmens Guild", cost={"stone": 2, "ore": 1}, location=["left", "right"], victory_points=2, activity=["Gray"])
    traders_guild = Guild(3, "Purple", "4+", "Traders Guild", cost={"clay": 1, "papyrus": 1, "glass": 1}, location=["left", "right"], victory_points=1, activity=["Yellow"])
    philosophers_guild = Guild(3, "Purple", "4+", "Philosophers Guild", cost={"clay": 3, "papyrus": 1}, location=["left", "right"], victory_points=1, activity=["Green"])
    spies_guild = Guild(3, "Purple", "4+", "Spies Guild", cost={"clay": 3}, location=["left", "right"], victory_points=1, activity=["Red"])
    strategists_guild = Guild(3, "Purple", "4+", "Strategists Guild", cost={"ore": 2, "stone": 1}, location=["left", "right"], victory_points=1, activity=["defeat_token"])
    shipowners_guild = Guild(3, "Purple", "4+", "Shipowners Guild", cost={"wood": 3, "papyrus": 1}, location=["self"], victory_points=1, activity=["Brown", "Gray", "Purple"])
    scientists_guild = Guild(3, "Purple", "4+", "Scientists Guild", cost={"wood": 2, "ore": 2}, resource_choices={"choices": [{"compass": 1, "tablet": 1, "gear": 1}]})
    magistrates_guild = Guild(3, "Purple", "4+", "Magistrates Guild", cost={"wood": 3, "cloth": 1}, location=["left", "right"], victory_points=1, activity=["Blue"])
    builders_guild = Guild(3, "Purple", "4+", "Builders Guild", cost={"stone": 2, "clay": 1, "cloth": 1}, location=["self", "left", "right"], victory_points=1, activity=["Wonders"])

    if nr_of_players >= 4:
        return [workers_guild, craftmens_guild, traders_guild, philosophers_guild, spies_guild, strategists_guild, shipowners_guild, scientists_guild, magistrates_guild, builders_guild]
    else:
        return []
