from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('BlackJack')
root.geometry("1200x800")
root.configure(background="dark green")

class Card():#example

    BACK_OF_CARD_IMAGE = pygame.image.load('images/BackOfCard.png')

    def __init__(self, window, rank, suit, value):
        self.window = window
        self.rank = rank
        self.suit = suit
        self.cardName = rank + ' of ' + suit
        self.value = value
        fileName = 'images/' + self.cardName + '.png'
        # Set some starting location; use setLoc below to change
        self.images = pygwidgets.ImageCollection(window, (0, 0),
                                {'front': fileName,
                                 'back': Card.BACK_OF_CARD_IMAGE}, 'back')
        


    def shuffle():
    #reenable buttons
    hit_button.config(state="normal")
    
	stand_button.config(state="normal")

	global win_status, p_total, d_total
	
	win_status = {"dealer":"no", "player":"no"}

	#real time total of cards
	p_total = 0
	d_total = 0

	# Clear all the old cards from previous games
	dealer_label_1.config(image='')
	dealer_label_2.config(image='')
	dealer_label_3.config(image='')
	dealer_label_4.config(image='')
	dealer_label_5.config(image='')

	player_label_1.config(image='')
	player_label_2.config(image='')
	player_label_3.config(image='')
	player_label_4.config(image='')
	player_label_5.config(image='')


	# Define Our Deck
	suits = ["diamonds", "clubs", "hearts", "spades"]
	values = range(2, 15)
	# 11 = Jack, 12=Queen, 13=King, 14 = Ace

	global deck
	deck =[]

	for suit in suits:
		for value in values:
			deck.append(f'{value}_of_{suit}')

	# Create our players
	global dealer, player, dealer_spot, player_spot, d_score, p_score
	dealer = []
	player = []
	p_score=[]
	d_score=[]
	dealer_spot = 0
	player_spot = 0



	# Shuffle Cards for player and dealer
	dealer_hit()
	dealer_hit()
	player_hit()
	player_hit()

	# Put number of remaining cards in title bar
	root.title(f'BlackJack - {len(deck)} Cards Left')





        
class Deck():
    SUIT_TUPLE = ('Diamonds', 'Clubs', 'Hearts', 'Spades')
    # This dict maps each card rank to a value for a standard deck
    STANDARD_DICT = {'Ace':1, '2':2, '3':3, '4':4, '5':5,
                                  '6':6, '7':7, '8': 8, '9':9, '10':10,
                                  'Jack':11, 'Queen':12, 'King':13}

    def __init__(self, window, rankValueDict=STANDARD_DICT):
        # rankValueDict defaults to STANDARD_DICT, but you can call
        # with a different dict, e.g., a special dict for Blackjack
        self.startingDeckList = []
        self.playingDeckList = []
        for suit in Deck.SUIT_TUPLE:
            for rank, value in rankValueDict.items():
                oCard = Card(window, rank, suit, value)
                self.startingDeckList.append(oCard)

        self.shuffle()

class Game():
    CARD_OFFSET = 110
    CARDS_TOP = 300
    CARDS_LEFT = 75
    NCARDS = 8
    POINTS_CORRECT = 15
    POINTS_INCORRECT = 10