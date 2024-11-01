from .models import RawMaterial, ManufacturedGoods, CivilianStructures, ScientificStructures, CommercialStructures, MilitaryStructures

def generate_age_II_raw_material_cards():
    saw_mill1 = RawMaterial(2, "Brown", "3+", "Saw Mill", cost={"coins":1}, wood = 2)
    saw_mill2 = RawMaterial(2, "Brown", "3+", "Saw Mill", cost={"coins":1}, wood = 2)
    saw_mill3 = RawMaterial(2, "Brown", "3+", "Saw Mill", cost={"coins":1}, wood = 2)

    brickyard1 = RawMaterial(2, "Brown", "3+", "Brickyard", cost={"coins":1}, clay = 2)
    brickyard2 = RawMaterial(2, "Brown", "3+", "Brickyard", cost={"coins":1}, clay = 2)
    brickyard3 = RawMaterial(2, "Brown", "3+", "Brickyard", cost={"coins":1}, clay = 2)

    quarry1 = RawMaterial(2, "Brown", "3+", "Quarry", cost={"coins":1}, stone = 2)
    quarry2 = RawMaterial(2, "Brown", "3+", "Quarry", cost={"coins":1}, stone = 2)
    quarry3 = RawMaterial(2, "Brown", "3+", "Quarry", cost={"coins":1}, stone = 2)

    foudry1 = RawMaterial(2, "Brown", "3+", "Foundry", cost={"coins":1}, ore = 2)
    foudry2 = RawMaterial(2, "Brown", "3+", "Foundry", cost={"coins":1}, ore = 2)
    foudry3 = RawMaterial(2, "Brown", "3+", "Foundry", cost={"coins":1}, ore = 2)

def generate_age_II_manufactured_goods():
    glassblower1 = ManufacturedGoods(2, "Gray", "3+", "Glassblower", glass=1)
    glassblower2 = ManufacturedGoods(2, "Gray", "3+", "Glassblower", glass=1)

    drying_room1 = ManufacturedGoods(2, "Gray", "3+", "Drying Room", papyrus=1)
    drying_room2 = ManufacturedGoods(2, "Gray", "3+", "Drying Room", papyrus=1)
    
    return [glassblower1, glassblower2, drying_room1, drying_room2]

def generate_age_II_civilian_structures(nr_of_players):
    aqueduct1 = CivilianStructures(2, "Blue", "4+", "Altar", cost={"stone":3}, victory_points=5)
    aqueduct2 = CivilianStructures(2, "Blue", "4+", "Altar", cost={"stone":3}, victory_points=5)

    temple1 = CivilianStructures(2, "Blue", "3+", "Temple", cost={"wood":1, "clay":1, "glass":1}, victory_points=3)
    temple2 = CivilianStructures(2, "Blue", "3+", "Temple", cost={"wood":1, "clay":1, "glass":1}, victory_points=3)
    temple3 = CivilianStructures(2, "Blue", "3+", "Temple", cost={"wood":1, "clay":1, "glass":1}, victory_opoints=3)

    statue1 = CivilianStructures(2, "Blue", "4+", "Statue", cost={"ore":2, "wood":1}, victory_points=4)
    statue2 = CivilianStructures(2, "Blue", "4+", "Statue", cost={"ore":2, "wood":1}, victory_points=4)
    
    courthouse1 = CivilianStructures(2, "Blue", "4+", "Statue", cost={"clay":2, "cloth":1}, victory_points=4)
    courthouse2 = CivilianStructures(2, "Blue", "4+", "Statue", cost={"clay":2, "cloth":1}, victory_points=4)
    if nr_of_players > 3:
        return [temple1, temple2, temple3] + [aqueduct1, aqueduct2, statue1, statue2, courthouse1, courthouse2]

def generate_age_II_scientific_structures():
    library1 = ScientificStructures(2, "Green", "4+", "Library", cost={"stone":2, "cloth":1} tablet=1)
    library2 = ScientificStructures(2, "Green", "4+", "Library", cost={"stone":2, "cloth":1} tablet=1)

    dispensary1 = ScientificStructures(2, "Green", "3+", "Dispensary", cost={"ore":2, "glass":1} compass=1)
    dispensary2 = ScientificStructures(2, "Green", "3+", "Dispensary", cost={"ore":2, "glass":1} compass=1)

    school1 = ScientificStructures(2, "Green", "3+", "School", cost={"wood":1, "papyrus":1}, tablet=1)
    school2 = ScientificStructures(2, "Green", "3+", "School", cost={"wood":1, "papyrus":1}, tablet=1)

    labratory1 = ScientificStructures(2, "Green", "3+", "Labratory", cost={"clay":2, "papyrus":1}, gear=1)
    labratory2 = ScientificStructures(2, "Green", "3+", "Labratory", cost={"clay":2, "papyrus":1}, gear=1)
    if nr_of_players > 3:
        return [dispensary1, dispensary2, school1, school2, labratory1, labratory2] + [library1, library2]
    return [dispensary1, dispensary2, school1, school2, labratory1, labratory2]

def generate_age_II_commerical_structures(nr_of_players):
    caravansery1 = CommercialStructure(2, "Yellow", "3+", "Caravansery", cost={"wood":2}, resource_choices={"choices":[{"wood":1,"ore":1,"clay":1,"stone":1}]})
    caravansery2 = CommercialStructure(2, "Yellow", "3+", "Caravansery", cost={"wood":2}, resource_choices={"choices":[{"wood":1,"ore":1,"clay":1,"stone":1}]})
    caravansery3 = CommercialStructure(2, "Yellow", "3+", "Caravansery", cost={"wood":2}, resource_choices={"choices":[{"wood":1,"ore":1,"clay":1,"stone":1}]})

    forum1 = CommercialStructure(2, "Yellow", "3+", "Forum", cost={"clay":2}, resource_choices={"choices":[{"glass":1,"papyrus":1,"cloth":1}]})
    forum2 = CommercialStructure(2, "Yellow", "3+", "Forum", cost={"clay":2}, resource_choices={"choices":[{"glass":1,"papyrus":1,"cloth":1}]})
    forum3 = CommercialStructure(2, "Yellow", "3+", "Forum", cost={"clay":2}, resource_choices={"choices":[{"glass":1,"papyrus":1,"cloth":1}]})

    vineyard = CommercialStructure(2, "Yellow", "3+", "Vineyard", resource_choices= {"choices":[{"coin":1}], "condition":{"where":["left", "right", "self"], "what":"Brown"}})

    bazar = CommercialStructure(2, "Yellow", "4+", "Bazar", resource_choices= {"choices":[{"coin":2}], "condition":{"where":["left", "right", "self"], "what":"Yellow"}})
    if nr_of_players > 3:
        return [caravansery1, caravansery2, caravansery3, forum1, forum2, forum3, vineyard] + [bazar]
    return [caravansery1, caravansery2, caravansery3, forum1, forum2, forum3, vineyard]

def generate_age_II_millitary_structures(nr_of_players):
    walls1 = MillitaryStructure(2, "Red", "3+", "Walls", cost={"stone":3}, shield=2)
    walls2 = MillitaryStructure(2, "Red", "3+", "Walls", cost={"stone":3}, shield=2)

    training_ground1 = MillitaryStructure(2, "Red", "4+", "Training Ground", cost={"wood":1, "ore":1, "clay":1}, shield=2)
    training_ground2 = MillitaryStructure(2, "Red", "4+", "Training Ground", cost={"wood":1, "ore":1, "clay":1}, shield=2)

    stables1 = MillitaryStructure(2, "Red", "3+", "Stables", cost={"wood":1, "ore":1, "clay":1}, shield=1) #same cost as training_grounds? seems unreasonable
    stables2 = MillitaryStructure(2, "Red", "3+", "Stables", cost={"wood":1, "ore":1, "clay":1}, shield=1)
    stables3 = MillitaryStructure(2, "Red", "3+", "Stables", cost={"wood":1, "ore":1, "clay":1}, shield=1)

    archery_range1 = MillitaryStructure(2, "Red", "4+", "Stables", cost={"wood":2, "ore":1}, shield=2)
    archery_range2 = MillitaryStructure(2, "Red", "4+", "Stables", cost={"wood":2, "ore":1}, shield=2)
    if nr_of_players > 3:
        return [walls1, walls2, stables1, stables2, stables3] + [training_grond1, training_ground2, archery_range1, archery_range2]
    return [walls1, walls2, stables1, stables2, stables3]
