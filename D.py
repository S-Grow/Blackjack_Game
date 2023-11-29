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
            ace_index = self.score.index(11)
            self.score[ace_index] = 1
            score = sum(self.score)
        return score

    def check_for_ace_conversion(self):
        if 11 in self.score:
            ace_index = self.score.index(11)
            self.score[ace_index] = 1

class TitleScreen:
    def __init__(self, root, on_start_g):
        self.root = root
        self.on_start_g = on_start_g

        self.root.title('BlackJack - Title Screen')
        self.root.eval('tk::PlaceWindow . center')

        # Fullscreen
        #self.root.attributes('-fullscreen', True)

        self.title_frame = Frame(self.root, bg="dark green")
        self.title_frame.pack(expand=True, fill=BOTH)

        title_label = Label(self.title_frame, text="BlackJack", font=("Times New Roman", 36, "bold"), bg="dark green", fg="white")
        title_label.pack(pady=20)

        start_button = Button(self.title_frame, text="Place Your Bet", font=("Times New Roman", 18), command=self.start_bet)
        start_button.pack()

    def start_bet(self):
        self.title_frame.destroy()
        self.on_start_g()

class Betting:
    def __init__(self, root, on_start_game):
        self.root = root
        self.title_screen = TitleScreen(root, self.setup_game)
        self.on_start_game = on_start_game

    def setup_game(self):
        self.root.title('BlackJack - Betting')
        self.root.eval('tk::PlaceWindow . center')
        self.root.geometry("270x270")
        self.root.config(background='blue')
        self.betting_frame = Frame(self.root, bg="blue")
        self.betting_frame.grid()
    
        
        bet_label = Label(self.betting_frame, text="Betting:", font=("Times New Roman", 24, "bold"), bg="green", fg="white")
        bet_label.grid(column = 1, pady = 40)

        betinc_button = Button(self.betting_frame, text = "+", font = ("Times New Roman", 18), bg = "green", fg = "white", command = self.inc_bet)
        betinc_button.grid(row = 3, column = 2, padx = 20)

        betdec_button = Button(self.betting_frame, text="-", font=("Times New Roman", 18), bg="green", fg="white", command = self.dec_bet)
        betdec_button.grid(row = 3, padx = 20)

        currentbet_label = Label(self.betting_frame, text = (f"Current Bet: $0"), font = ("Times New Roman", 18), bg = "green", fg = "white")
        currentbet_label.grid()

        start_button = Button(self.betting_frame, text="Start Game", font=("Times New Roman", 18), command=self.start_game)
        start_button.grid(column = 1, pady = 30)
    
    def inc_bet(self):
        self.current_bet += 10
        self.update_bet()

    def dec_bet(self):
        if self.current_bet == 0:
            pass
        else:
            self.current_bet -= 10
            self.update_bet()

    def update_bet(self):
        current_bet = self.current_bet
        self.currentbet_label.config(text=f"Current Bet: ${current_bet}")
        

class BlackjackGame():
    def __init__(self, root):
        self.root = root
        self.title_screen = Betting(root, self.setup_game)

    def setup_game(self):
        self.root.title('BlackJack')

        # Set window size based on screen resolution
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        window_position_x = (screen_width - window_width) // 2
        window_position_y = (screen_height - window_height - 50) // 2
        self.root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")
        

        self.root.configure(background="dark green")

        self.deck = None
        self.dealer = None
        self.player = None
        self.dealer_spot = 0
        self.player_spot = 0
        self.win_status = {"dealer": "no", "player": "no"}
        self.blackjack_occurred = False

        self.create_frames()
        self.create_buttons()
        self.shuffle()

    def create_frames(self):
        self.my_frame = Frame(self.root, bg="dark green")
        self.my_frame.pack(pady=20)

        self.dealer_frame = LabelFrame(self.my_frame, text="Dealer", bd=0)
        self.dealer_frame.pack(padx=20, ipadx=20)

        self.player_frame = LabelFrame(self.my_frame, text="Player", bd=0)
        self.player_frame.pack(ipadx=20, pady=10)

        self.dealer_labels = [Label(self.dealer_frame, text='') for _ in range(5)]
        for i, label in enumerate(self.dealer_labels):
            label.grid(row=1, column=i, pady=20, padx=20)

        self.player_labels = [Label(self.player_frame, text='') for _ in range(5)]
        for i, label in enumerate(self.player_labels):
            label.grid(row=1, column=i, pady=20, padx=20)

        self.card_images = []

        self.player_score_label = Label(self.player_frame, text="Score: 0", font=("Times New Roman", 12), bg="dark green", fg="white")
        self.player_score_label.grid(row=0, column=0, padx=10, pady=10)

        self.dealer_score_label = Label(self.dealer_frame, text=f"Score: 0", font=("Times New Roman", 12), bg="dark green", fg="white")
        self.dealer_score_label.grid(row=0, column=0, padx=10, pady=10)

    def create_buttons(self):
        self.button_frame = Frame(self.root, bg="dark green")
        self.button_frame.pack(pady=15)

        self.shuffle_button = Button(self.button_frame, text="Shuffle", font=("Times New Roman", 14), command=self.shuffle)
        self.shuffle_button.grid(row=0, column=0)

        self.hit_button = Button(self.button_frame, text="Hit", font=("Times New Roman", 14), command=self.player_hit)
        self.hit_button.grid(row=0, column=1, padx=10)

        self.stand_button = Button(self.button_frame, text="Stand", font=("Times New Roman", 14), command=self.stand)
        self.stand_button.grid(row=0, column=2)

    def shuffle(self):
        self.deck = Deck()
        self.dealer = Player()
        self.player = Player()
        self.win_status = {"dealer": "no", "player": "no"}
        self.blackjack_occurred = False
        self.clear_cards()

        self.dealer_hit()
        self.player_hit()
        self.dealer_hit()
        self.player_hit()

        self.hit_button.config(state="normal")
        self.stand_button.config(state="normal")

        self.root.title(f'BlackJack - {len(self.deck.cards)} Cards Left')
        self.update_card_images()

    def clear_cards(self):
        for label in self.dealer_labels + self.player_labels:
            label.config(image='')

        self.dealer_spot = 0
        self.player_spot = 0

    def resize_cards(self, card):
        our_card_img = Image.open(card)
        our_card_resize_image = our_card_img.resize((150, 218))
        our_card_image = ImageTk.PhotoImage(our_card_resize_image)
        self.card_images.append(our_card_image)
        return our_card_image

    def update_card_images(self):
        for i in range(self.dealer_spot):
            if i == 0 and not self.blackjack_occurred:
                dealer_image = self.resize_cards('images/cards/back_of_card.png')
            else:
                dealer_card = self.dealer.hand[i]
                dealer_image = self.resize_cards(f'images/cards/{dealer_card}.png')
            self.dealer_labels[i].config(image=dealer_image)

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
                self.blackjack_occurred = True
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
                messagebox.showinfo("Push!", "Both hands are equal pushed!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()
            elif self.win_status["dealer"] == "yes":
                messagebox.showinfo("Dealer Wins", "Oh No! Dealer got Blackjack!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()
            elif self.win_status["player"] == "yes":
                messagebox.showinfo("Player Wins", "Blackjack! You Win!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()
        else:
            if self.win_status["dealer"] == "yes" and self.win_status["player"] == "yes":
                messagebox.showinfo("Push!", "Both hands are equal pushed!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()
            elif self.win_status["player"] == "bust":
                messagebox.showinfo("Player Bust", f"You Bust, You Lose! {self.p_total}!")
                self.hit_button.config(state="disabled")
                self.stand_button.config(state="disabled")
                self.flip_first_card()

        self.update_scores()

    def stand(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")
        self.flip_first_card()

        while self.dealer.calculate_score() < 17:
            self.dealer_hit()
        self.update_scores()
        self.check_winner()
        self.update_dealer_score()

    def dealer_hit(self):
        if self.dealer_spot < 5 and self.win_status["dealer"] == "no":
            try:
                dealer_card = self.deck.draw_card()
                self.dealer.receive_card(dealer_card)

                if self.dealer_spot == 0:
                    self.first_dealer_card = dealer_card
                    self.dealer_image1 = self.resize_cards('images/cards/back_of_card.png')
                    self.dealer_labels[0].config(image=self.dealer_image1)
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

        self.check_five_cards_winner()

    def check_winner(self):
        p_total = self.player.calculate_score()

        if p_total == 21:
            messagebox.showinfo("Player Wins", "your hand is higher! You Win!")
        elif p_total > 21:
            messagebox.showinfo("Player Bust", f"You Bust, You Lose! {p_total}!")
        elif self.dealer.calculate_score() == 21:
            messagebox.showinfo("Dealer Wins", "Oh No! Dealers hand is better!")
        elif self.dealer.calculate_score() > 21:
            messagebox.showinfo("Dealer Bust", "Dealer Busts! You Win!")
        elif self.dealer.calculate_score() > p_total:
            messagebox.showinfo("Dealer Wins", "Dealer has a higher score. You Lose!")
        elif self.dealer.calculate_score() < p_total:
            messagebox.showinfo("Player Wins", "You have a higher score. You Win!")
        else:
            messagebox.showinfo("Push!", "It's a push! Nobody wins.")

        self.update_scores()

    def update_scores(self):
        player_score = self.player.calculate_score()
        self.player_score_label.config(text=f"Score: {player_score}")

        dealer_score = self.dealer.calculate_score()
        self.dealer_score_label.config(text=f"Score: ? + {dealer_score - self.dealer.score[0]}")

    def update_dealer_score(self):
        dealer_score = self.dealer.calculate_score()
        self.dealer_score_label.config(text=f"Score: {dealer_score}")

    def check_five_cards_winner(self):
        if self.player_spot == 5 and self.player.calculate_score() < 21:
            messagebox.showinfo("Player Wins", "You have 5 cards and your score is less than 21. You Win!")
            self.hit_button.config(state="disabled")
            self.stand_button.config(state="disabled")
            self.flip_first_card()





# Initialize Tkinter
root = Tk()

# Create the Blackjack game
game = BlackjackGame(root)

# Run the Tkinter main loop
root.mainloop()
