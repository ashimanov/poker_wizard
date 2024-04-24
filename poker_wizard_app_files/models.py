
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']
suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']




# creates an instance of a player, which has 2 attributes - a name and a hand of cards
class Player:

    def __init__(self, name):
        self.name = name
        self.player_hand = []

    def player_cards(self, card): # adding a card to player's hand
        self.player_hand.append(card)


# creates an instance of the game
# 12 players max, player1 = app user (find these settings in the logic.py)
class Game:
    def __init__(self):
        self.id: None
        self.active = True
        self.deck = []
        self.round = None
        self.community_cards = []
        self.cards_posted = {0: False, 1: False, 2: False, 3: False} # own cards posted to the game (each round)

        for rank in ranks: # making a list of tuples representing a fresh full deck of 52 cards
            for suit in suits:
                self.deck.append((rank, suit))


input_card_ranks = {
    '2': 'Two',
    '3': 'Three',
    '4': 'Four',
    '5': 'Five',
    '6': 'Six',
    '7': 'Seven',
    '8': 'Eight',
    '9': 'Nine',
    'T': 'Ten',
    'J': 'Jack',
    'Q': 'Queen',
    'K': 'King',
    'A': 'Ace',
}

input_card_suits = {
    'S': 'Spades',
    'C': 'Clubs',
    'D': 'Diamonds',
    'H': 'Hearts'
}