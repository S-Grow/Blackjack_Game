from tkinter import *
import random
from PIL import Image, ImageTk


root = Tk()
root.title('BlackJack')
root.geometry("1200x800")
root.configure(background="green")

# Resize Cards
def resize_cards(card):
	# Open the image
	our_card_img = Image.open(card)

	# Resize The Image
	our_card_resize_image = our_card_img.resize((150, 218))
	
	# output the card
	global our_card_image
	our_card_image = ImageTk.PhotoImage(our_card_resize_image)

	# Return that card
	return our_card_image

# Shuffle The Cards
def shuffle():
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
	values = ["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"]
	# 11 = Jack, 12=Queen, 13=King, 14 = Ace

	global deck
	deck =[]

	for suit in suits:
		for value in values:
			deck.append(f'{value}_of_{suit}')

	# Create our players
	global dealer, player, dealer_spot, player_spot
	dealer = []
	player = []
	dealer_spot = 0
	player_spot = 0



	# Shuffle Cards for player and dealer
	dealer_hit()
	dealer_hit()
	player_hit()
	player_hit()

	# Put number of remaining cards in title bar
	root.title(f'BlackJack - {len(deck)} Cards Left')

def dealer_hit():
	global dealer_spot
	if dealer_spot < 5:
		try:
			# Get the player Card
			dealer_card = random.choice(deck)
			# Remove Card From Deck
			deck.remove(dealer_card)
			# Append Card To Dealer List
			dealer.append(dealer_card)
			# Output Card To Screen
			global dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5
			
			
			if dealer_spot == 0:
				# Resize Card
				dealer_image1 = resize_cards(f'images/cards/{dealer_card}.png')
				# Output Card To Screen
				dealer_label_1.config(image=dealer_image1)
				# Increment our player spot counter
				dealer_spot += 1
			elif dealer_spot == 1:
				# Resize Card
				dealer_image2 = resize_cards(f'images/cards/{dealer_card}.png')
				# Output Card To Screen
				dealer_label_2.config(image=dealer_image2)
				# Increment our player spot counter
				dealer_spot += 1
			elif dealer_spot == 2:
				# Resize Card
				dealer_image3 = resize_cards(f'images/cards/{dealer_card}.png')
				# Output Card To Screen
				dealer_label_3.config(image=dealer_image3)
				# Increment our player spot counter
				dealer_spot += 1
			elif dealer_spot == 3:
				# Resize Card
				dealer_image4 = resize_cards(f'images/cards/{dealer_card}.png')
				# Output Card To Screen
				dealer_label_4.config(image=dealer_image4)
				# Increment our player spot counter
				dealer_spot += 1
			elif dealer_spot == 4:
				# Resize Card
				dealer_image5 = resize_cards(f'images/cards/{dealer_card}.png')
				# Output Card To Screen
				dealer_label_5.config(image=dealer_image5)
				# Increment our player spot counter
				dealer_spot += 1

			# Put number of remaining cards in title bar
			root.title(f'BlackJack - {len(deck)} Cards Left')

		except:
			root.title(f'BlackJack - No Cards In Deck')

def player_hit():
	global player_spot
	if player_spot < 5:
		try:
			# Get the player Card
			player_card = random.choice(deck)
			# Remove Card From Deck
			deck.remove(player_card)
			# Append Card To Dealer List
			player.append(player_card)
			# Output Card To Screen
			global player_image1, player_image2, player_image3, player_image4, player_image5
			
			
			if player_spot == 0:
				# Resize Card
				player_image1 = resize_cards(f'images/cards/{player_card}.png')
				# Output Card To Screen
				player_label_1.config(image=player_image1)
				# Increment our player spot counter
				player_spot += 1
			elif player_spot == 1:
				# Resize Card
				player_image2 = resize_cards(f'images/cards/{player_card}.png')
				# Output Card To Screen
				player_label_2.config(image=player_image2)
				# Increment our player spot counter
				player_spot += 1
			elif player_spot == 2:
				# Resize Card
				player_image3 = resize_cards(f'images/cards/{player_card}.png')
				# Output Card To Screen
				player_label_3.config(image=player_image3)
				# Increment our player spot counter
				player_spot += 1
			elif player_spot == 3:
				# Resize Card
				player_image4 = resize_cards(f'images/cards/{player_card}.png')
				# Output Card To Screen
				player_label_4.config(image=player_image4)
				# Increment our player spot counter
				player_spot += 1
			elif player_spot == 4:
				# Resize Card
				player_image5 = resize_cards(f'images/cards/{player_card}.png')
				# Output Card To Screen
				player_label_5.config(image=player_image5)
				# Increment our player spot counter
				player_spot += 1

			# Put number of remaining cards in title bar
			root.title(f'BlackJack - {len(deck)} Cards Left')

		except:
			root.title(f'BlackJack - No Cards In Deck')


# Deal Out Cards
def deal_cards():
	try:
		# Get the deler Card
		card = random.choice(deck)
		# Remove Card From Deck
		deck.remove(card)
		# Append Card To Dealer List
		dealer.append(card)
		# Output Card To Screen
		global dealer_image
		dealer_image = resize_cards(f'images/cards/{card}.png')
		dealer_label.config(image=dealer_image)
		#dealer_label.config(text=card)

		# Get the player Card
		card = random.choice(deck)
		# Remove Card From Deck
		deck.remove(card)
		# Append Card To Dealer List
		player.append(card)
		# Output Card To Screen
		global player_image
		player_image = resize_cards(f'images/cards/{card}.png')
		player_label.config(image=player_image)
		#player_label.config(text=card)


		# Put number of remaining cards in title bar
		root.title(f'BlackJack - {len(deck)} Cards Left')

	except:
		root.title(f'BlackJack - No Cards In Deck')




my_frame = Frame(root, bg="green")
my_frame.pack(pady=20)

# Create Frames For Cards
dealer_frame = LabelFrame(my_frame, text="Dealer Score = ?", bd=0)
dealer_frame.pack(padx=20, ipadx=20)

player_frame = LabelFrame(my_frame, text="Player Score = ", bd=0)
player_frame.pack(ipadx=20, pady=10)

# Put Dealer cards in frames
dealer_label_1 = Label(dealer_frame, text='')
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = Label(dealer_frame, text='')
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = Label(dealer_frame, text='')
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = Label(dealer_frame, text='')
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = Label(dealer_frame, text='')
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)

# Put Player cards in frames
player_label_1 = Label(player_frame, text='')
player_label_1.grid(row=1, column=0, pady=20, padx=20)

player_label_2 = Label(player_frame, text='')
player_label_2.grid(row=1, column=1, pady=20, padx=20)

player_label_3 = Label(player_frame, text='')
player_label_3.grid(row=1, column=2, pady=20, padx=20)

player_label_4 = Label(player_frame, text='')
player_label_4.grid(row=1, column=3, pady=20, padx=20)

player_label_5 = Label(player_frame, text='')
player_label_5.grid(row=1, column=4, pady=20, padx=20)

# Create Frame for buttons
button_frame = Frame(root, bg="green")
button_frame.pack(pady=20)

# Create a couple buttons
shuffle_button = Button(button_frame, text="Shuffle", font=("Times New Roman", 14), command=shuffle)
shuffle_button.grid(row=0, column=0)

card_button = Button(button_frame, text="Hit", font=("Times New Roman", 14), command=player_hit)
card_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand", font=("Times New Roman", 14))
stand_button.grid(row=0, column=2)

#frame for betting buttons
bet_frame = Frame(root, bg="green")
bet_frame.pack(pady=20)

increase_bet = Button(bet_frame, text="+", font=("Times New Roman", 14))
increase_bet.grid(row=1, column=3)

decrease_bet = Button(bet_frame, text="-", font=("Times New Roman", 14))
decrease_bet.grid(row=1, column=1)

bet_amount= Label(bet_frame, text='$0', font=("Times New Roman", 16))
bet_amount.grid(row=1, column=2, padx=5)

bet_button = Button(bet_frame, text="Place Bet", font=("Times New Roman", 14)) #, command=place_bet)
bet_button.grid(row=2, column=2)


# Shuffle Deck On Start
shuffle()


root.mainloop()