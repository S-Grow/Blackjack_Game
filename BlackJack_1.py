from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox


root = Tk()
root.title('BlackJack')
root.geometry("1200x800")
root.configure(background="dark green")

# Resize Cards
def resize_cards(card):
	# Opens the image
	our_card_img = Image.open(card)

	# Resize
	our_card_resize_image = our_card_img.resize((150, 218))
	
	# output the card
	global our_card_image
	our_card_image = ImageTk.PhotoImage(our_card_resize_image)

	# Returns card
	return our_card_image

def flip_first_card():
	dealer_image1 = resize_cards(f'images/cards/{first_dealer_card}.png')
	# Output Card To Screen
	dealer_label_1.config(image=dealer_image1)

def BlackJack_Check(hand):
	global p_total, d_total
	#resets running total
	p_total = 0
	d_total = 0


	if hand =="dealer":
		if len(d_score) == 2:
			if sum(d_score)== 21:
				
				win_status["dealer"] = "yes"


	if hand == "player":
		if len(p_score) == 2:
			if sum(p_score) == 21:
				
				win_status["player"] = "yes"

		else:
			# Loop thru player score list and add up cards
			for score in p_score:
				# Add up score
				p_total += score

			if p_total == 21:
				win_status["player"] = "yes"
			
			elif p_total > 21:
				# Check for ace conversion
				for card_num, card in enumerate(p_score):
					if card == 11:
						p_score[card_num] = 1

						# Clear player total and recalculate
						p_total = 0
						for score in p_score:
							# Add up score
							p_total += score
						
						# Check for over 21
						if p_total > 21:
							win_status["player"] = "bust"
				else:
					# Check new totals for 21 or over 21
					if p_total == 21:
						win_status["player"] = "yes"
					if p_total > 21:
						win_status["player"] = "bust"


	if len(d_score) == 2 and len(p_score) == 2:
		# Check For a Tie
		if win_status["dealer"] == "yes" and win_status["player"] == "yes":
			#tie
			messagebox.showinfo("Push!", "both hands are BlackJack pushed!")
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			flip_first_card()
			
		
		# Check for Dealer Win
		elif win_status["dealer"] == "yes":
			messagebox.showinfo("Dealer Wins", "Oh No! Dealer got BlackJack!")
			# Disable buttons
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			# Resize Card
			flip_first_card()

		# Check For Player Win
		elif win_status["player"] == "yes":
			messagebox.showinfo("Player Wins", "Blackjack! You Win!")
			# Disable buttons
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			flip_first_card()

	
	else:
		if win_status["dealer"] == "yes" and win_status["player"] == "yes":
			#tie
			messagebox.showinfo("Push!", "both hands are equal pushed!")
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			flip_first_card()
		
		# Check for Dealer Win
		
		#elif win_status["dealer"] == "yes":
			#messagebox.showinfo("Dealer Wins", "Oh No! Dealer got 21!")
			# Disable buttons
			#hit_button.config(state="disabled")
			#stand_button.config(state="disabled")
			# Resize Card
			#dealer_image1 = resize_cards(f'images/cards/{first_dealer_card}.png')#need to find a way to show the actual card
			# Output Card To Screen
			#dealer_label_1.config(image=dealer_image1)
		

		# Check For Player Win
		elif win_status["player"] == "yes":
			messagebox.showinfo("Player Wins", "21! You Win!")
			# Disable buttons
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			flip_first_card()

	if win_status["player"] == "bust":
			messagebox.showinfo("Player Bust", f"You Bust, You Lose! {p_total}!")
			# Disable buttons
			hit_button.config(state="disabled")
			stand_button.config(state="disabled")
			flip_first_card()


def stand():
	global p_total, d_total
	p_total = 0
	d_total = 0
	messagebox.showinfo("Stand?", "PlaceHolder_txt")

# Shuffle The Cards
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

			#append to dealer score for face cards
			dcard = int(dealer_card.split("_", 1)[0])
			if dcard == 14:
				d_score.append(11)
			elif dcard == 11 or dcard == 12 or dcard == 13:
				d_score.append(10)
			else:
				d_score.append(dcard)
			# Output Card To Screen
			global first_dealer_card,dealer_image1, dealer_image2, dealer_image3, dealer_image4, dealer_image5
			
			
			if dealer_spot == 0:
				# Resize Card
				first_dealer_card=dealer_card
				dealer_image1 = resize_cards(f'images/cards/back_of_card.png')
				#dealer_image1 = resize_cards(f'images/cards/{first_dealer_card}.png')
				
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

		BlackJack_Check("dealer")

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

			# append player score 
			pcard = int(player_card.split("_", 1)[0])
			if pcard == 14:
				p_score.append(11)
			elif pcard == 11 or pcard == 12 or pcard == 13:
				p_score.append(10)
			else:
				p_score.append(pcard)

			

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

		BlackJack_Check("player")

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
		

		# Get the player Card
		card = random.choice(deck)
		# Remove Card From Deck
		deck.remove(card)
		# Append Card To Dealer List
		player.append(card)
		# Output Card To Screen
		global player_image
		player_image = resize_cards(f'images/cards/{card}.png')
		


		# Put number of remaining cards in title bar
		root.title(f'BlackJack - {len(deck)} Cards Left')

	except:
		root.title(f'BlackJack - No Cards In Deck')




my_frame = Frame(root, bg="dark green")
my_frame.pack(pady=20)

# Create Frames For Cards
dealer_frame = LabelFrame(my_frame, text="Dealer ", bd=0)
dealer_frame.pack(padx=20, ipadx=20)

x = 1 #frames will need to be moved to update for score as it changes or new frame spesfic to scores need to be created
y = 1
player_frame = LabelFrame(my_frame, text=(f"Player Score = {x} + {y} "), bd=0)
player_frame.pack(ipadx=20, pady=10)

# Put Dealer cards in frames
dealer_label_1 = Label(dealer_frame, text='',)
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
button_frame = Frame(root,bg="dark green")
button_frame.pack(pady=15)

# Create action buttons
shuffle_button = Button(button_frame, text="Shuffle", font=("Times New Roman", 14), command=shuffle)
shuffle_button.grid(row=0, column=0)

hit_button = Button(button_frame, text="Hit", font=("Times New Roman", 14), command=player_hit)
hit_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand", font=("Times New Roman", 14), command=stand)
stand_button.grid(row=0, column=2)

#frame for betting buttons
bet_frame = Frame(root, bg="dark green")
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