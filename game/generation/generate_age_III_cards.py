from .models import RawMaterial, ManufacturedGoods, CivilianStructures, ScientificStructures, CommercialStructures, MilitaryStructures

def generate_age_III_CivilianStructures(nr_of_players):
    pantheon1 = ManufacturedGoods(3, "Blue", "4+", "Pantheon", cost={"clay":2, "papyrus":1, "glass":1, "cloth":1}, victory_points=7)
    pantheon2 = ManufacturedGoods(3, "Blue", "4+", "Pantheon", cost={"clay":2, "papyrus":1, "glass":1, "cloth":1}, victory_points=7)

    gardens1 = ManufacturedGoods(3, "Blue", "3+", "Gardens", cost={"wood":2, "clay":1}, victory_points=5)
    gardens2 = ManufacturedGoods(3, "Blue", "3+", "Gardens", cost={"wood":2, "clay":1}, victory_points=5)

    town_hall1 = ManufacturedGoods(3, "Blue", "3+", "Town Hall", cost={"stone":2, "ore"1, "glass":1}, victory_points=6)
    town_hall2 = ManufacturedGoods(3, "Blue", "3+", "Town Hall", cost={"stone":2, "ore"1, "glass":1}, victory_points=6)

    palace1 = ManufacturedGoods(3, "Blue", "5+", "Town Hall", cost={"wood":1, "clay":1, "stone":1, "ore"1, "glass":1, "cloth":1, "papyrus":1}, victory_points=8)

    senate1 = ManufacturedGoods(3, "Blue", "3+", "Senate", cost={"wood":2, "ore":1, "stone":1}, victory_points=6)
    senate2 = ManufacturedGoods(3, "Blue", "3+", "Senate", cost={"wood":2, "ore":1, "stone":1}, victory_points=6)
    if nr_of_players >= 4:
        if nr_of_players >= 5:
            return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2] + [pantheon1, pantheon2] + [palace1]
        return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2] + [pantheon1, pantheon2]
    return [gardens1, gardens2, town_hall1, town_hall2, senate1, senate2]

def generate_age_III_scientific_structures(nr_of_players):
    lodge1 = ScientificStructures(3, "Green", "3+", "Lodge", cost={"clay":2, "papyrus":1, "cloth":1}, compass=1)
    lodge2 = ScientificStructures(3, "Green", "3+", "Lodge", cost={"clay":2, "papyrus":1, "cloth":1}, compass=1)

    observatory1 = ScientificStructures(3, "Green", "4+", "Observatory", cost={"ore":2, "glass":1, "cloth":1}, gear=1)
    observatory2 = ScientificStructures(3, "Green", "4+", "Observatory", cost={"ore":2, "glass":1, "cloth":1}, gear=1)

    university1 = ScientificStructures(3, "Green", "3+", "University", cost={"wood":2, "glass":1, "papyrus":1}, tablet=1)
    university2 = ScientificStructures(3, "Green", "3+", "University", cost={"wood":2, "glass":1, "papyrus":1}, tablet=1)
    
    academy1 = ScientificStructures(3, "Green", "4+", "Academy", cost={"stone":3, "glass":1}, compass=1)
    academy2 = ScientificStructures(3, "Green", "4+", "Academy", cost={"stone":3, "glass":1}, compass=1)

    study1 = ScientificStructures(3, "Green", "3+", "Study", cost={"wood":1, "papyrus":1, "cloth":1}, gear=1)
    study2 = ScientificStructures(3, "Green", "3+", "Study", cost={"wood":1, "papyrus":1, "cloth":1}, gear=1)
    if nr_of_players >= 4:
        return [lodge1, lodge2, university1, university2, study1, study2] + [observatory1, observatory2, academy1, academy2]
    return [lodge1, lodge2, university1, university2, study1, study2]

def generate_age_III_commerical_structures(nr_of_players):
    haven1 = CommercialStructure(3, "Yellow", "3+", "Haven", cost={"wood":1, "ore":1, "cloth":1},
            resource_choices= {"choices":[{"coin":1}, {"victory_point":1}], "condition":{"where":["self"], "what":"Brown"}})
    haven2 = CommercialStructure(3, "Yellow", "3+", "Haven", cost={"wood":1, "ore":1, "cloth":1},
            resource_choices= {"choices":[{"coin":1}, {"victory_point":1}], "condition":{"where":["self"], "what":"Brown"}})

    lighthouse1 = CommercialStructure(3, "Yellow", "3+", "Lighthouse", cost={"stone":1, "glass":1},
            resource_choices= {"choices":[{"coin":1}, {"victory_point":1}], "condition":{"where":["self"], "what":"Yellow"}})
    lighthouse2 = CommercialStructure(3, "Yellow", "3+", "Lighthouse", cost={"stone":1, "glass":1},
            resource_choices= {"choices":[{"coin":1}, {"victory_point":1}], "condition":{"where":["self"], "what":"Yellow"}})

    chamber_of_commerce1 = CommercialStructure(3, "Yellow", "4+", "Chamber Of Commerce", cost={"clay":2, "papyru":1},
            resource_choices= {"choices":[{"coin":3}, {"victory_point":2}], "condition":{"where":["self"], "what":"Gray"}})
    chamber_of_commerce2 = CommercialStructure(3, "Yellow", "4+", "Chamber Of Commerce", cost={"clay":2, "papyru":1},
            resource_choices= {"choices":[{"coin":3}, {"victory_point":2}], "condition":{"where":["self"], "what":"Gray"}})

    arena1 = CommercialStructure(3, "Yellow", "3+", "Arena", cost={"stone":2, "ore":1},
            resource_choices= {"choices":[{"coin":3}, {"victory_point":1}], "condition":{"where":["self"], "what":"stage of wonders"}})
    arena2 = CommercialStructure(3, "Yellow", "3+", "Arena", cost={"stone":2, "ore":1},
            resource_choices= {"choices":[{"coin":3}, {"victory_point":1}], "condition":{"where":["self"], "what":"stage of wonders"}})
    if nr_of_players >= 4:
        return [haven1, haven2, lighouse1, lighthouse2, arena1, arena2] + [chamber_of_commerce1, chamber_of_commerce2]
    return [haven1, haven2, lighouse1, lighthouse2, arena1, arena2]

def generate_age_II_millitary_structures(nr_of_players):
    fortifications1 = MillitaryStructure(3, "Red", "3+", "Fortifications", cost={"stone":3, "ore":1}, shield=3)
    fortifications2 = MillitaryStructure(3, "Red", "3+", "Fortifications", cost={"stone":3, "ore":1}, shield=3)

    circus1 = MillitaryStructure(3, "Red", "4+", "Circus", cost={"clay":3, "ore":1}, shield=3)
    circus2 = MillitaryStructure(3, "Red", "4+", "Circus", cost={"clay":3, "ore":1}, shield=3)

    arsenal1 = MillitaryStructure(3, "Red", "4+", "Arsenal", cost={"wood":2, "ore":1, "cloth":1}, shield=2)
    arsenal2 = MillitaryStructure(3, "Red", "4+", "Arsenal", cost={"wood":2, "ore":1, "cloth":1}, shield=2)

    siege_workshop1 = MillitaryStructure(3, "Red", "3+", "Siege Workshop", cost={"wood":3, "clay":1}, shield=2)
    siege_workshop2 = MillitaryStructure(3, "Red", "3+", "Siege Workshop", cost={"wood":3, "clay":1}, shield=2)
    if nr_of_players >= 4:
        return [fortifications1, fortifications2, siege_workshop1, siege_workshop2] + [circus1, circus2, arsenal1, arsenal2]
    return [fortifications1, fortifications2, siege_workshop1, siege_workshop2]

def generate_age_III_guilds(nr_of_players):
    workers_guild = Guilds(3, "Purple", "4+", "Workers Guild", cost={"ore":2, "clay":1}, where=["left", "right"], victory_points=1, what=["Brown"])
    craftmens_guild = Guilds(3, "Purple", "4+", "Craftmens Guild", cost={"stone":2, "ore":1}, where=["left", "right"], victory_points=2, what=["Gray"])
    traders_guild = Guilds(3, "Purple", "4+", "Traders Guild", cost={"clay":1, "payrus":1, "glass":1}, where=["left", "right"], victory_points=1, what=["Yellow"])
    philosophers_guild = Guilds(3, "Purple", "4+", "Philosophers Guild", cost={"clay":3, "payrus":1}, where=["left", "right"], victory_points=1, what=["Green"])
    spies_guild = Guilds(3, "Purple", "4+", "Spies Guild", cost={"clay":3}, where=["left", "right"], victory_points=1, what=["Red"])
    strategists_guild = Guilds(3, "Purple", "4+", "Strategists Guild", cost={"ore":2, "stone":1}, where=["left", "right"], victory_points=1, what=["defeat_token"])
    shipowners_guild = Guilds(3, "Purple", "4+", "Shipowners Guild", cost={"wood":3, "papyrus":1}, where=["self"], victory_points=1, what=["Brown", "Gray", "Purple"])
    scientists_guild = Guilds(3, "Purple", "4+", "Scientists Guild", cost={"wood":2, "ore":2}, resource_choices={"choices":[{"compass":1, "tablet":1, "gear":1}]})
    magistrates_guild = Guilds(3, "Purple", "4+", "Magistrates Guild", cost={"wood":3, "cloth":1}, where=["left", "right"], victory_points=1, what=["Blue"])
    builders_guild = Guilds(3, "Purple", "4+", "Builders Guild", cost={"stone":2, "clay":1, "cloth":1}, where=["self","left", "right"], victory_points=1, what=["Wonders"])
    if nr_of_players >= 5:
        return [workers_guild, craftmens_guild, traders_guild, philosophers_guild, spies_guild, strategists_guild, shipowners_guild, scientists_guild, magistrates_guild, builders_guild]


