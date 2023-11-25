from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

root = Tk()
root.title('BlackJack')
root.geometry("1200x800")
root.configure(background="dark green")

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
dealer_label_1 = Label(dealer_frame, text='',bg="blue")
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
shuffle_button = Button(button_frame, text="Shuffle", font=("Times New Roman", 14))#, command=shuffle)
shuffle_button.grid(row=0, column=0)

hit_button = Button(button_frame, text="Hit", font=("Times New Roman", 14))#, command=player_hit)
hit_button.grid(row=0, column=1, padx=10)

stand_button = Button(button_frame, text="Stand", font=("Times New Roman", 14))#, command=stand)
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
#shuffle()


root.mainloop()


