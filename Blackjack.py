# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        hand = "Hand contains "
        
        for card in self.hand:
            hand += str(card) + " "
        return hand

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        aces = False
        
        for card in self.hand:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                aces = True
        
        if not aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
    
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_number = 0
        for card in self.hand:
            if pos[1] == 310 and card_number == 0 and in_play == True:
                # draw card back
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                                  [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]],
                                  CARD_BACK_SIZE)
            else:
                card.draw(canvas, [pos[0] + (card_number % 7) * 77, pos[1] + (card_number // 7) * 102])
            card_number += 1        
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        deck = "Deck contains "
        for card in self.deck:
            deck += str(card) + " "
        return deck


#define event handlers for buttons
def deal():
    global deck, outcome, in_play, player_hand, dealer_hand, score
    # your code goes here
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    dealer_hand = Hand()

    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())

    if in_play:
        score -= 1
        outcome = "You lost the round! New round: Hit or stand?"
    else:
        outcome = "Hit or stand?"

    in_play = True
    

def hit():
    global deck, in_play, outcome, player_hand, score
    # if the hand is in play, hit the player
    
    if in_play:
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() <= 21:
            outcome = "Hit or stand?"
        else:
            outcome = "You're busted!"
            score -= 1
            in_play = False
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    global deck, in_play, dealer_hand, player_hand, outcome, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        in_play = False
        if player_hand.get_value() > 21:
            outcome = "You have busted!"
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            score += 1
            outcome = "You won! Deal again?"
        elif dealer_hand.get_value() >= player_hand.get_value():
            score -= 1
            outcome = "Tie means dealer wins! Deal again?"
        else:
            score += 1
            outcome = "You won! Deal again?"


# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text("Blackjack", [162,	80], 70, "Black")
    
    canvas.draw_text("Player", [10, 145], 24, "Black")
    canvas.draw_text("Dealer", [10, 295], 24, "Black")
    canvas.draw_text("Score: " + str(score), [500, 25], 24, "Yellow")
#    canvas.draw_text("Game # " + str(numb_game), [500, 45], 21, "White")
    canvas.draw_text(outcome, [90, 575], 24, "White")

    # draw cards
    player_hand.draw(canvas, [10, 160])
    dealer_hand.draw(canvas, [10, 310])

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
