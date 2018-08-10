#Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
loses = 0
wins = 0
player_hand = []
dealer_hand = []
# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank

        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
        print type (rank)


    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        hand_str = ""
        for card in self.hand:
            hand_str += str (card)+ " "
        return  hand_str

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        global  hand_value, player_hand, dealer_hand
        rank=0
        hand_value = 0
        for card in self.hand:
            rank = card.get_rank()
            hand_value += VALUES[rank]
        for card in self.hand:
            if rank == 'A' and hand_value<11:
                hand_value +=10
        return hand_value

    def draw(self, canvas, pos):
        global player_hand, dealer_hand
        for card in self.hand:
            card.draw (canvas, [pos[0] ,pos[1]])
            pos [0] += 100


# define deck class
class Deck:
    def __init__(self):
       self.deck = []
       for s in SUITS :
           for r in RANKS:
                self.deck.append(Card(s, r))

    def shuffle(self):
        random.shuffle (self.deck)


    def deal_card(self):
        self.choice = random.choice(self.deck)
        return  self.choice

    def __str__(self):
        deck_str = ""
        for card in self.deck:
            deck_str += str (card)+ " "
        return  deck_str




#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player_hand, dealer_hand, loses
    deck= Deck()
    player_hand=Hand()
    dealer_hand=Hand()
    deck.shuffle()
    i= 0
    while i < 2:
       player_hand.add_card (deck.deal_card())
       dealer_hand.add_card (deck.deal_card())
       i +=1
    outcome = random.choice (["Hit! no no Stand!hit? stand?", "Hit?Stand?what you gonna do?", "should you Stand or should you Hit?"])
    if in_play:
        loses+=1
        outcome ="you have lost the last round"
    in_play = True
    return player_hand, dealer_hand

def hit():
    global  outcome, in_play, deck, player_hand, dealer_hand, loses
    deck= Deck()
    value = 0
    card = (deck.deal_card())
    player_hand.add_card (card)
    value = player_hand.get_value()
    if value <= 21:
        outcome = random.choice (["Hit! no no Stand!hit? stand?", "Hit?Stand?what you gonna do?", "should you Stand or should you Hit?"])
    elif in_play and value > 21:
        in_play = False
        loses +=1
        outcome = "You have busted, new deal?  "



def stand():
    global loses, wins,  outcome, in_play
    if not in_play :
          outcome = "You have busted, new deal?  "

    elif in_play :
        while dealer_hand.get_value() < 17 :
              card = (deck.deal_card())
              dealer_hand.add_card (card)
        dealer = dealer_hand.get_value()
        player = player_hand.get_value()
        in_play = False
        if dealer> 21:
           wins +=1
           outcome = "the dealer have busted, new deal?  "
        elif dealer <= 21 and dealer > player:
            loses +=1
            outcome = "The dealer wins! new deal?"
        else:
            wins +=1
            outcome = "you wins!new deal?"


    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    global wins, loses
    hand = Hand()
    player_hand.draw(canvas, [100, 450])
    dealer_hand.draw(canvas, [100, 150])
    canvas.draw_text(outcome, (20, 375), 36, "red")
    canvas.draw_text( "Blackjack", (200, 50), 54, "black")
    if in_play:
       canvas.draw_image(card_back, CARD_BACK_CENTER , CARD_BACK_SIZE , (136.5, 199), CARD_BACK_SIZE)
    canvas.draw_text("Player", (100, 425), 36, "black")
    canvas.draw_text("Dealer", (20, 100), 36, "red")
    canvas.draw_text("score: "+str(wins-loses), (400, 100), 36, "red")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)



# get things rolling
deal()
frame.start()
