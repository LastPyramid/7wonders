from django.db import models
class Game:
    def __init__(self, age_I_cards, age_II_cards, age_III_cards, players):
        self.turn = 1
        self.age_I_cards = age_I_cards
        self.age_II_cards = age_II_cards
        self.age_III_cards = age_III_cards
        self.players = players
    
    def pick_card(self, player, deck): #remove?
        pass
    
    def start_game(self): #remove?
        pass

class Resources:
    def __init__(self, ore=0, wood=0, clay=0, stone=0, glass=0, papyrus=0, cloth=0):
        self.ore = ore
        self.wood = wood
        self.clay = clay
        self.stone = stone
        self.glass = glass
        self.papyrus = papyrus
        self.cloth = cloth

class Player():
    def __init__(self, wonder, name):
        #self.number = number
        self.wonder = wonder
        self.name = name
        self.resources = {}
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

class Card:
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None):
        self.age = age
        self.color = color
        self.number_of_players = number_of_players
        self.name = name
        self.cost = cost or {}
        self.symbol = symbol
        self.resource_choices = resource_choices or {}

class RawMaterial(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, wood=0, stone=0, clay=0, ore=0):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.wood = wood
        self.stone = stone
        self.clay = clay
        self.ore = ore

class ManufacturedGood(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, glass=None, papyrus=None, cloth=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.glass = glass
        self.papyrus = papyrus
        self.cloth = cloth

class CivilianStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, victory_points=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.victory_points = victory_points

class ScientificStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, compass=None, gear=None, tablet=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.compass = compass
        self.gear = gear
        self.tablet = tablet

class CommercialStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, west_trading=None, east_trading=None, marketplace=None, gold=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.gold = gold
        self.west_trading = west_trading
        self.east_trading = east_trading
        self.marketplace = marketplace

class MilitaryStructure(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, shield=0):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.shield = shield

class Guild(Card):
    def __init__(self, age, color, number_of_players, name, cost=None, symbol=None, resource_choices=None, location=None, activity=None, victory_points=None, compass=None, gear=None, tablet=None):
        super().__init__(age, color, number_of_players, name, cost, symbol, resource_choices)
        self.location = location
        self.activity = activity
        self.victory_points = victory_points
        self.compass = compass
        self.gear = gear
        self.tablet = tablet

class Wonder():
    def __init__(self, name, benefit, stage1, stage2, stage3=None, stage4=None):
        self.name = name
        self.benefit = benefit
        self.stage1 = stage1
        self.stage2 = stage2
        self.stage3 = stage3
        self.stage4 = stage4

class Stage:
    def __init__(self, benefit, cost):
        self.benefit = benefit
        self.cost = cost
