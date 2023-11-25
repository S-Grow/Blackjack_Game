from tkinter import *
import random
from PIL import Image, ImageTk
from tkinter import messagebox

class Deck:
    def __init__(self):
        suits = ["diamonds", "clubs", "hearts", "spades"]
        values = range(2, 15)
        self.cards = [f'{value}_of_{suit}' for suit in suits for value in values]
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            raise IndexError("No cards left in the deck")
        return self.cards.pop()


class Player:
    def __init__(self):
        self.hand = []
        self.score = []

    def receive_card(self, card):
        self.hand.append(card)
        card_value = int(card.split("_", 1)[0])
        if card_value == 14:
            self.score.append(11)
        elif 11 <= card_value <= 13:
            self.score.append(10)
        else:
            self.score.append(card_value)

    def calculate_score(self):
        score = sum(self.score)
        if score > 21 and 11 in self.score:
            # Convert one Ace from 11 to 1
            ace_index = self.score.index(11)
            self.score[ace_index] = 1
            score = sum(self.score)
        return score

    def check_for_ace_conversion(self):
        if 11 in self.score:
            ace_index = self.score.index(11)
            self.score[ace_index] = 1


class BlackjackGame:
    def __init__(self, root):
        self.root = root
        self.root.title('BlackJack')
        self.root.geometry("1200x800")
        self.root.configure(background="dark green")

        self.deck = None
        self.dealer = None
        self.player = None
        self.dealer_spot = 0
        self.player_spot = 0
        self.win_status = {"dealer": "no", "player": "no"}
        self.blackjack_occurred = False  # Added variable for blackjack

        self.create_frames()
        self.create_buttons()
        self.shuffle()

    def create_frames(self):
        # Frame for cards
        self.my_frame = Frame(self.root, bg="dark green")
        self.my_frame.pack(pady=20)

        # Dealer frame
        self.dealer_frame = LabelFrame(self.my_frame, text="Dealer ", bd=0)
        self.dealer_frame.pack(padx=20, ipadx=20)

        # Player frame
        self.player_frame = LabelFrame(self.my_frame, text="Player Score = 0", bd=0)
        self.player_frame.pack(ipadx=20, pady=10)

        # Put Dealer cards in frames
        self.dealer_labels = [Label(self.dealer_frame, text='') for _ in range(5)]
        for i, label in enumerate(self.dealer_labels):
            label.grid(row=0, column=i, pady=20, padx=20)

        # Put Player cards in frames
        self.player_labels = [Label(self.player_frame, text='') for _ in range(5)]
        for i, label in enumerate(self.player_labels):
            label.grid(row=1, column=i, pady=20, padx=20)

        # Keep a reference to the images
        self.card_images = []

    def create_buttons(self):
        # Frame for buttons
        self.button_frame = Frame(self.root, bg="dark green")
        self.button_frame.pack(pady=15)

        # Action buttons
        self.shuffle_button = Button(self.button_frame, text="Shuffle", font=("Times New Roman", 14), command=self.shuffle)
        self.shuffle_button.grid(row=0, column=0)

        self.hit_button = Button(self.button_frame, text="Hit", font=("Times New Roman", 14), command=self.player_hit)
        self.hit_button.grid(row=0, column=1, padx=10)

        self.stand_button = Button(self.button_frame, text="Stand", font=("Times New Roman", 14), command=self.stand)
        self.stand_button.grid(row=0, column=2)

    def shuffle(self):
        # Reset variables and clear old cards
        self.deck = Deck()
        self.dealer = Player()
        self.player = Player()
        self.win_status = {"dealer": "no", "player": "no"}
        self.blackjack_occurred = False  # Reset blackjack variable
        self.clear_cards()

        # Deal initial cards
        self.dealer_hit()
        self.player_hit()
        self.dealer_hit()
        self.player_hit()

        # Re-enable buttons
        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

        # Update title with remaining cards
        self.root.title(f'BlackJack - {len(self.deck.cards)} Cards Left')

        # Update card images
        self.update_card_images()

    def clear_cards(self):
        for label in self.dealer_labels + self.player_labels:
            label.config(image='')

        # Reset counters
        self.dealer_spot = 0
        self.player_spot = 0

    def resize_cards(self, card):
        # Resize cards
        our_card_img = Image.open(card)
        our_card_resize_image = our_card_img.resize((150, 218))
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        self.card_images.append(our_card_image)
        return our_card_image

    def update_card_images(self):
        # Update dealer card images
        for i in range(self.dealer_spot):
            if i == 0 and not self.blackjack_occurred:
                dealer_image = self.resize_cards(f'images/cards/back_of_card.png')
                
            else:
                dealer_card = self.dealer.hand[i - 1]
                dealer_image = self.resize_cards(f'images/cards/{dealer_card}.png')
            self.dealer_labels[i].config(image=dealer_image)

        # Update player card images
        for i in range(self.player_spot):
            player_card = self.player.hand[i]
            player_image = self.resize_cards(f'images/cards/{player_card}.png')
            self.player_labels[i].config(image=player_image)

    def flip_first_card(self):
        if not self.blackjack_occurred:
            dealer_image1 = self.resize_cards(f'images/cards/{self.first_dealer_card}.png')
            self.dealer_labels[0].config(image=dealer_image1)

    def BlackJack_Check(self, hand):
        if hand == "dealer":
            if len(self.dealer.score) == 2 and sum(self.dealer.score) == 21:
                self.win_status["dealer"] = "yes"
                self.blackjack_occurred = True  # Set the variable when blackjack occurs
        elif hand == "player":
            if len(self.player.score) == 2 and sum(self.player.score) == 21:
                self.win_status["player"] = "yes"
            else:
                self.p_total = self.player.calculate_score()
                if self.p_total == 21:
                    self.win_status["player"] = "yes"
                elif self.p_total > 21:
                    self.player.check_for_ace_conversion()
                    self.p_total = self.player.calculate_score()
                    if self.p_total > 21:
                        self.win_status["player"] = "bust"
                    else:
                        if self.p_total == 21:
                            self.win_status["player"] = "yes"
                        if self.p_total > 21:
                            self.win_status["player"] = "bust"

        if len(self.dealer.score) == 2 and len(self.player.score) == 2:
            if self.win_status["dealer"] == "yes" and self.win_status["player"] == "yes":
                messagebox.showinfo("Push!", "both hands are equal pushed!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()  # Call flip_first_card here
            elif self.win_status["dealer"] == "yes":
                messagebox.showinfo("Dealer Wins", "Oh No! Dealer got BlackJack!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()  # Call flip_first_card here
            elif self.win_status["player"] == "yes":
                messagebox.showinfo("Player Wins", "Blackjack! You Win!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()  # Call flip_first_card here
        else:
            if self.win_status["dealer"] == "yes" and self.win_status["player"] == "yes":
                messagebox.showinfo("Push!", "both hands are equal pushed!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()  # Call flip_first_card here
            elif self.win_status["player"] == "bust":
                messagebox.showinfo("Player Bust", f"You Bust, You Lose! {self.p_total}!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()  # Call flip_first_card here

    def stand(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.flip_first_card()  # Call flip_first_card here

        # Dealer's turn to draw cards until reaching 17 or 21
        x=True
        while x:
            if self.dealer.calculate_score() < 17:
                self.dealer_hit()
            else:
                x=False
        self.d_total = self.dealer.calculate_score()
        if self.dealer.calculate_score() >= 17:
            if self.dealer.calculate_score() < 22:
                self.check_winner()

    def dealer_hit(self):
        if self.dealer_spot < 5:
            try:
                dealer_card = self.deck.draw_card()
                self.dealer.receive_card(dealer_card)

                if self.dealer_spot == 0:
                    self.first_dealer_card = dealer_card
                    self.dealer_image1 = self.resize_cards(f'images/cards/back_of_card.png')
                    self.dealer_labels[1].config(image=self.dealer_image1)  # Update the correct label
                    self.dealer_spot += 1
                else:
                    dealer_image = self.resize_cards(f'images/cards/{dealer_card}.png')
                    self.dealer_labels[self.dealer_spot].config(image=dealer_image)
                    self.dealer_spot += 1

                self.root.title(f'BlackJack - {len(self.deck.cards)} Cards Left')

            except IndexError:
                self.root.title(f'BlackJack - No Cards In Deck')

            self.BlackJack_Check("dealer")

    def player_hit(self):
        if self.player_spot < 5:
            try:
                player_card = self.deck.draw_card()
                self.player.receive_card(player_card)

                player_image = self.resize_cards(f'images/cards/{player_card}.png')
                self.player_labels[self.player_spot].config(image=player_image)
                self.player_spot += 1

                self.root.title(f'BlackJack - {len(self.deck.cards)} Cards Left')

            except IndexError:
                self.root.title(f'BlackJack - No Cards In Deck')

            self.BlackJack_Check("player")

    def check_winner(self):
        p_total = self.player.calculate_score()

        if p_total == 21:
            messagebox.showinfo("Player Wins", "Blackjack! You Win!")
        elif p_total > 21:
            messagebox.showinfo("Player Bust", f"You Bust, You Lose! {p_total}!")
        elif self.d_total == 21:
            messagebox.showinfo("Dealer Wins", "Oh No! Dealer got Blackjack!")
        elif self.d_total > 21:
            messagebox.showinfo("Dealer Bust", "Dealer Busts! You Win!")
        elif self.d_total > p_total:
            messagebox.showinfo("Dealer Wins", "Dealer has a higher score. You Lose!")
        elif self.d_total < p_total:
            messagebox.showinfo("Player Wins", "You have a higher score. You Win!")
        else:
            messagebox.showinfo("Push!", "It's a push! Nobody wins.")

# Create an instance of the BlackjackGame class
root = Tk()
game = BlackjackGame(root)
root.mainloop()
