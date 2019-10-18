from random import choice
start_cash = 500

class Card:
    def __init__(self, value, suit, face_up=True):
        self.value = value
        self.suit = suit
        self.face_up = face_up
        
    def getSuit(self):
        return self.suit.title()
    
    def getValue(self):
        if isinstance(self.value, int):
            return self.value
        elif self.value == 'A':
            return 11
        else:
            return 10
        
    def setFaceDown(self):
        self.face_up = False
        
class Player:
    def __init__(self, name, hand=set([]), cash = start_cash):
        self.name = name
        self.hand = hand
        self.cash = cash
        
    def getName(self):
        return self.name
        
    def getHand(self):
        return self.hand
        
    def getCash(self):
        return self.cash
    
    def setCash(self, bet, bet_won):
        if bet_won:
            self.cash += bet
        else:
            self.cash -= bet
            
    def addCard(self, card):
        self.hand.add(Card(value,suit))
        
    def checkHandValue(self):
        hand_value = 0
        aces = 0
        for card in self.hand:
            hand_value += card.getValue()
            if card.getValue() == 11:
                aces += 1
        if hand_value <= 21:
            return hand_value
        elif aces != 0:
            while hand_value > 21 and aces != 0:
                aces -= 1
                hand_value -= 10
            if hand_value <= 21:
                return hand_value
            else:
                return 'bust'
        else:
            return 'bust'
            
        
class Settings:
    def __init__(self, start_cash=500, min_bet=0, players=1):
        self.start_cash = start_cash
        self.min_bet = min_bet
        self.players = players
        
    def getSettings(self):
        return start_cash, min_bet, players
    
    def setStartCash(self, value):
        if isinstance(value, int) and value > self.min_bet:
            self.start_cash = value
            message = f'The starting cash was updated sucessfully to {value}!'
        else:
            message = 'Make sure to select a number greater than the minimum bet!'
        return message
        
    def setMinBet(self, value):
        if isinstance(value, int) and value < self.start_cash and value >= 0:
            self.min_bet = value
            message = f'The minimum bet was updated successfully to {value}!'
        else:
            message = 'Make sure to select a nonnegative number less than the starting cash.'
        return message
        
    def setPlayers(self, value):
        if isinstance(value, int) and value >= 1:
            self.players = value
            message = f'You\'re ready to play with {value} players!'
        else:
            message = 'You\'ll need at least 1 player to try and beat the dealer!'
        return message
    
class Blackjack:
    def __init__(self, settings=Settings):
        self.start_cash, self.min_bet, self.players = settings.getSettings()
        
    def instantiateDeck(self):
        deck = set([])
        suits = set(['spades', 'hearts', 'diamonds', 'clubs'])
        values = set([2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'])
        for value in values:
            for suit in suits:
                for i in range(7):
                    deck.add(Card(value, suit))
        return deck
    
    def generateCard(self, deck):
        card = choice(tuple(deck))
        deck.remove(card)
        return card
    
    def dealHands(self):
        for player in self.players:
            player.addCard(self.generateCard(deck).setFaceDown())
            player.addCard(self.generateCard(deck))
    def playGame():
            
            
    
    
    
    
game = Blackjack('hi')
deck = game.instantiateDeck()
print(len(deck))
card = game.generateCard(deck)
print(card.getValue(), card.getSuit())
print(len(deck))
