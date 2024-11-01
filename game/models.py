from django.db import models

class Game(models.Model):
    def start_game(self):
        pass
class Player(models.Model):
    def __init__(self, wonder, deck):
        self.coins = coins
        self.wonder = wonder
        self.stage_of_wonder = 0
        self.deck = []
        self.free_construction = []
        self.ore
        self.wood
        self.clay
        self.stone
        self.glass
        self.papyrus
        self.cloth
        self.compass
        self.gear
        self.scriptorium
        self.west_trading
        self.east_trading
        self.marketplace
        self.conflict_token
        self.victory_points
        self.defeat_token
class Card:
    def __init__(self, age, color, number_of_players, name, cost=None):
        self.age = age
        self.color = color
        self.number_of_players = number_of_players
        self.name = name
        self.cost = cost if cost else {}
class RawMaterial(Card): #Brown
    def __init__(self, *args, wood=None, stone=None, clay=None, ore=None):
        super().__init__(*args)
        self.wood = wood
        self.stone = stone
        self.clay = clay
        self.ore = ore
class ManufacturedGoods(Card): #Grey
    def __init__(self, *args, glass=None, papyrus=None, cloth=None):
        super().__init__(*args)
        self.glass = glass
        self.papyrus = papyrus
        self.cloth = cloth
class CivilianStructures(Card): #Blue
    def __init__(self, *args, victory_points):
        super().__init__(*args)
        self.victory_points = victory_points
class ScientificStructures(Card): #Green
    def __init__(self, *args, compass=None, gear=None, scriptorium=None):
        super().__init__(*args)
        self.compass = compass
        self.gear = gear
        self.scriptorium = scriptorium
class CommercialStructures(Card): #Yellow
    def __init__(self, *args, west_trading=None, east_trading=None, marketplace=None, gold=None, resource_choices=None):
        super().__init__(*args)
        self.gold = gold
        self.west_trading = west_trading
        self.east_trading = east_trading
        self.marketplace = marketplace
        self.resource_choices = resource_choices

class MilitaryStructures(Card): #Red
    def __init__(self, *args, shield):
        super().__init__(*args)
        self.shield = shield
class Guilds(Card): #Purple
    def __init__(self, *args, where, what, victory_points=None, compass=None, gear=None, tablet=None):
        super().__init__(*args)
        self.where = where #maybe rename these
        self.what = what
        self.victory_points = victory_points
        self.resource_choices = resource_choices # should we have a clas for this?
class Wonder:
    def __init__(self, stage1, stage2, stage3):
        self.stage1 = stage1
        self.stage2 = stage2
        self.stage3 = stage3
#I think we sohuld maybe make like a production class something that tells us what it produces. uhm, isnt that "RawMaterial?"
