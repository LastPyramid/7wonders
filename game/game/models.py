from django.db import models
class Game:
    def __init__(self, age_I_cards, age_II_cards, age_III_cards, players):
        self.turn = 1
        self.age_I_cards = age_I_cards
        self.age_II_cards = age_II_cards
        self.age_III_cards = age_III_cards
        self.players = players
    
    def to_dict(self):
        return {
            "turn": self.turn,
            "age_I_cards": [card.to_dict() for card in self.age_I_cards],
            "age_II_cards": [card.to_dict() for card in self.age_II_cards],
            "age_III_cards": [card.to_dict() for card in self.age_III_cards],
            "players": [player.to_dict() for player in self.players],
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            age_I_cards=[Card.from_dict(card) for card in data["age_I_cards"]],
            age_II_cards=[Card.from_dict(card) for card in data["age_II_cards"]],
            age_III_cards=[Card.from_dict(card) for card in data["age_III_cards"]],
            players=[Player.from_dict(player) for player in data["players"]],
        )

class Resources:
    def __init__(self, ore=0, wood=0, clay=0, stone=0, glass=0, papyrus=0, cloth=0):
        self.ore = ore
        self.wood = wood
        self.clay = clay
        self.stone = stone
        self.glass = glass
        self.papyrus = papyrus
        self.cloth = cloth

    def to_dict(self):
        return {
            "ore": self.ore,
            "wood": self.wood,
            "clay": self.clay,
            "stone": self.stone,
            "glass": self.glass,
            "papyrus": self.papyrus,
            "cloth": self.cloth,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            ore=data.get("ore", 0),
            wood=data.get("wood", 0),
            clay=data.get("clay", 0),
            stone=data.get("stone", 0),
            glass=data.get("glass", 0),
            papyrus=data.get("papyrus", 0),
            cloth=data.get("cloth", 0),
        )

class Player():
    def __init__(self, wonder, name):
        #self.number = number
        self.wonder = wonder
        self.name = name
        self.resources = Resources() # This will not be shared right?
        self.cards = []
        self.cards_to_pick_from = []
        self.free_construction = []
        self.stage_of_wonder = 0
        self.coins = 3
        self.compass = 0
        self.gear = 0
        self.scriptorium = 0
        self.west_trading = False
        self.east_trading = False
        self.marketplace = False
        self.conflict_token = 0
        self.victory_points = 0
        self.defeat_token = 0

    def to_dict(self):
        wonder = None
        if isinstance(self.wonder, list):
            wonder = [wonder.to_dict() for wonder in self.wonder]
        elif isinstance(self.wonder, Wonder):
            wonder = self.wonder.to_dict()
        else:
            raise Exception("wonder in the game is neither a list nor a wonder objcet")

        return {
            "wonder": wonder,
            "name": self.name,
            "resources": self.resources.to_dict(),
            "cards": [card.to_dict() for card in self.cards],
            "cards_to_pick_from": [card.to_dict() for card in self.cards_to_pick_from],
            "free_construction": [construction.to_dict() for construction in self.free_construction],
            "stage_of_wonder": self.stage_of_wonder,
            "coins": self.coins,
            "compass": self.compass,
            "gear": self.gear,
            "scriptorium": self.scriptorium,
            "west_trading": self.west_trading,
            "east_trading": self.east_trading,
            "marketplace": self.marketplace,
            "conflict_token": self.conflict_token,
            "victory_points": self.victory_points,
            "defeat_token": self.defeat_token,
        }

    @classmethod
    def from_dict(cls, data):
        wonder = data["wonder"]
        if isinstance(wonder, list):
            wonder = [Wonder.from_dict(w) for w in wonder]
        else:
            wonder = Wonder.from_dict(wonder)
        player = cls(
            wonder=wonder,
            name=data["name"],
        )
        player.resources = Resources.from_dict(data.get("resources"))
        player.cards = [Card.from_dict(card) for card in data.get("cards", [])]
        player.cards_to_pick_from = [Card.from_dict(card) for card in data.get("cards_to_pick_from", [])]
        player.free_construction = [Card.from_dict(construction) for construction in data.get("free_construction", [])]
        player.stage_of_wonder = data.get("stage_of_wonder", 0)
        player.coins = data.get("coins", 3)
        player.compass = data.get("compass", 0)
        player.gear = data.get("gear", 0)
        player.scriptorium = data.get("scriptorium", 0)
        player.west_trading = data.get("west_trading", False)
        player.east_trading = data.get("east_trading", False)
        player.marketplace = data.get("marketplace", False)
        player.conflict_token = data.get("conflict_token", 0)
        player.victory_points = data.get("victory_points", 0)
        player.defeat_token = data.get("defeat_token", 0)
        return player

class Card:
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None):
        self.age = age
        self.color = color
        self.number_of_players = number_of_players
        self.name = name
        self.cost = cost or {}
        self.symbol = symbol
        self.resource_choices = resource_choices or {}
    
    def to_dict(self):
        return {
            "age": self.age,
            "color": self.color,
            "number_of_players": self.number_of_players,
            "name": self.name,
            "cost": self.cost,
            "symbol": self.symbol,
            "resource_choices": self.resource_choices,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            age=data["age"],
            color=data["color"],
            number_of_players=data["number_of_players"],
            name=data["name"],
            cost=data.get("cost", {}),
            symbol=data.get("symbol"),
            resource_choices=data.get("resource_choices", {}),
        )

class RawMaterial(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, wood=0, stone=0, clay=0, ore=0):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.wood = wood
        self.stone = stone
        self.clay = clay
        self.ore = ore

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "wood": self.wood,
            "stone": self.stone,
            "clay": self.clay,
            "ore": self.ore,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            wood=data.get("wood", 0),
            stone=data.get("stone", 0),
            clay=data.get("clay", 0),
            ore=data.get("ore", 0),
        )

class ManufacturedGood(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, glass=None, papyrus=None, cloth=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.glass = glass
        self.papyrus = papyrus
        self.cloth = cloth

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "glass": self.glass,
            "papyrus": self.papyrus,
            "cloth": self.cloth,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            glass=data.get("glass"),
            papyrus=data.get("papyrus"),
            cloth=data.get("cloth"),
        )

class CivilianStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, victory_points=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.victory_points = victory_points
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "victory_points": self.victory_points,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            victory_points=data.get("victory_points"),
        )
    

class ScientificStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, compass=None, gear=None, tablet=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.compass = compass
        self.gear = gear
        self.tablet = tablet

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            compass=data.get("compass"),
            gear=data.get("gear"),
            tablet=data.get("tablet"),
        )

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "compass": self.compass,
            "gear": self.gear,
            "tablet": self.tablet,
        })
        return data

class CommercialStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, west_trading=None, east_trading=None, marketplace=None, gold=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.gold = gold
        self.west_trading = west_trading
        self.east_trading = east_trading
        self.marketplace = marketplace

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "gold":self.gold,
            "west_trading":self.west_trading,
            "east_trading":self.east_trading,
            "marketplace":self.marketplace
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            gold=card.gold,
            west_trading=card.west_trading,
            east_trading=card.east_trading,
            marketplace=card.marketplace
        )
    
class MilitaryStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, shield=0):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.shield = shield

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "shield": self.shield,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            gold=data.get("gold"),
            west_trading=data.get("west_trading"),
            east_trading=data.get("east_trading"),
            marketplace=data.get("marketplace"),
        )

class Guild(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, location=None, activity=None, victory_points=None, compass=None, gear=None, tablet=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.location = location
        self.activity = activity
        self.victory_points = victory_points
        self.compass = compass
        self.gear = gear
        self.tablet = tablet

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "location": self.location,
            "activity": self.activity,
            "victory_points": self.victory_points,
            "compass": self.compass,
            "gear": self.gear,
            "tablet": self.tablet,
        })
        return data

    @classmethod
    def from_dict(cls, data):
        card = super().from_dict(data)
        return cls(
            age=card.age,
            color=card.color,
            number_of_players=card.number_of_players,
            name=card.name,
            cost=card.cost,
            symbol=card.symbol,
            resource_choices=card.resource_choices,
            location=data.get("location"),
            activity=data.get("activity"),
            victory_points=data.get("victory_points"),
            compass=data.get("compass"),
            gear=data.get("gear"),
            tablet=data.get("tablet"),
        )



class Wonder():
    def __init__(self, name, benefit, stage1, stage2, stage3=None, stage4=None):
        self.name = name
        self.benefit = benefit
        self.stage1 = stage1
        self.stage2 = stage2
        self.stage3 = stage3
        self.stage4 = stage4
    def to_dict(self):
        return {
            "name": self.name,
            "benefit": self.benefit,
            "stage1": self.stage1.to_dict() if self.stage1 else None,
            "stage2": self.stage2.to_dict() if self.stage2 else None,
            "stage3": self.stage3.to_dict() if self.stage3 else None,
            "stage4": self.stage4.to_dict() if self.stage4 else None,
        }

    @classmethod
    def from_dict(cls, data):
        stage1 = Stage.from_dict(data["stage1"]) if "stage1" in data else None # remove if here ?
        stage2 = Stage.from_dict(data["stage2"]) if "stage2" in data else None # remove if here ?
        stage3 = Stage.from_dict(data["stage3"]) if "stage3" in data and data["stage3"] != None else None
        stage4 = Stage.from_dict(data["stage4"]) if "stage4" in data and data["stage4"] != None else None
        return cls(
            name = data["name"],
            benefit = data["benefit"],
            stage1 = stage1,
            stage2 = stage2,
            stage3 = stage3,
            stage4 = stage4,
        )

class Stage:
    def __init__(self, benefit, cost):
        self.benefit = benefit
        self.cost = cost

    def to_dict(self):
        return {
            "benefit": self.benefit,
            "cost": self.cost,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            benefit=data["benefit"],
            cost=data["cost"],
        )