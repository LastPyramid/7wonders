from .models import RawMaterial, ManufacturedGood, CivilianStructure, ScientificStructure, CommercialStructure, MilitaryStructure, Player, Game
from ..generation.generate_age_I_cards import generate_age_I_cards
from ..generation.generate_age_II_cards import generate_age_II_cards
from ..generation.generate_age_III_cards import generate_age_III_cards
from ..generation.generate_age_III_cards import generate_age_III_cards
from ..generation.generate_wonders import generate_wonders
import random

def setup_game(nr_of_players):
	wonders = generate_wonders()
	random.shuffle(wonders)
	age_I_cards = generate_age_I_cards(nr_of_players)
	random.shuffle(age_I_cards)
	age_II_cards = generate_age_II_cards(nr_of_players)
	random.shuffle(age_II_cards)
	age_III_cards = generate_age_III_cards(nr_of_players)
	random.shuffle(age_III_cards)
	
	players = []	
	
	#Create players
	for number in range(nr_of_players):
		player = Player(number, wonders.pop())
		players.append(player)
	
    # Give players cards
	for player in players:
		for card in range(7):
			player.cards_to_pick_from.append(age_I_cards.pop())	

	game = Game(age_I_cards, age_II_cards, age_III_cards, players)
	return game
			
def play(game):
    pass

		
		
