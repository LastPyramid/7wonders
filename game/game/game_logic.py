from .models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure, Player, Game
from ..generation.generate_age_I_cards import generate_age_I_cards
from ..generation.generate_age_II_cards import generate_age_II_cards
from ..generation.generate_age_III_cards import generate_age_III_cards
from ..generation.generate_age_III_cards import generate_age_III_cards
from ..generation.generate_wonders import generate_wonders
import random

def setup_game(list_of_players):
	wonders = generate_wonders()
	nr_of_players = len(list_of_players)
	random.shuffle(wonders)
	age_I_cards = generate_age_I_cards(nr_of_players)
	random.shuffle(age_I_cards)
	age_II_cards = generate_age_II_cards(nr_of_players)
	random.shuffle(age_II_cards)
	age_III_cards = generate_age_III_cards(nr_of_players)
	random.shuffle(age_III_cards)
	
	players = []	
	picking_choices = {}
	
	#Create players
	for id, name in enumerate(list_of_players):
		player = Player(wonders.pop(), name, id)
		picking_choices[name] = None
		players.append(player)

	left_player = players[-1]
	for i in range(len(players)-1):
		right_player = players[i+1]
		players[i].left_player = left_player
		players[i].right_player = right_player
		left_player = players[i]
	players[-1].left_player = players[-2]
	players[-1].right_player = players[0]

	
    # Give players cards
	for player in players:
		for card in range(7):
			player.cards_to_pick_from.append(age_I_cards.pop())	

	game = Game(age_I_cards, age_II_cards, age_III_cards, picking_choices, players)
	return game

def start_age_II(game):
	for player in game.players:
		player.cards_to_pick_from = []
		for card in range(7):
			player.cards_to_pick_from.append(game.age_II_cards.pop())

def start_age_III(game):
	for player in game.players:
		player.cards_to_pick_from = []
		for card in range(7):
			player.cards_to_pick_from.append(game.age_III_cards.pop())