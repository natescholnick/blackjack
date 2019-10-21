from IPython.display import clear_output
from random import choice

start_cash = 500

class Card:
    def __init__(self, value, suit, face_up=True):
        self.value = value
        self.suit = suit
        self.face_up = face_up
        
    def getName(self):
        if self.value == 'J':
            return f'Jack of {self.suit}'
        elif self.value == 'Q':
            return f'Queen of {self.suit}'
        elif self.value == 'K':
            return f'King of {self.suit}'
        elif self.value == 'A':
            return f'Ace of {self.suit}'
        else:
            return f'{self.value} of {self.suit}'
    
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
    def __init__(self, name, hand=set([]), cash = start_cash, dealer=False):
        self.name = name
        self.hand = hand
        self.cash = cash
        self.dealer = dealer
    
    def getName(self):
        return self.name
        
    def getCash(self):
        return self.cash
    
    def setCash(self, cash):
        self.cash += cash
            
    def clearHand(self):
        self.hand = set([])
            
    def getHand(self):
        return self.hand
            
    def addCard(self, card):
        self.hand.add(card)
        
    def checkHandValue(self):
        bust = False
        hand_value = 0
        aces = 0
        for card in self.hand:
            hand_value += card.getValue()
            if card.getValue() == 11:
                aces += 1
        if hand_value <= 21:
            return hand_value, bust
        elif aces != 0:
            while hand_value > 21 and aces != 0:
                aces -= 1
                hand_value -= 10
            if hand_value <= 21:
                return hand_value, bust
            else:
                bust = True
                return hand_value, bust
        else:
            bust = True
            return hand_value, bust
            
        
class Settings:
    def __init__(self, start_cash=500, min_bet=0, players=1):
        self.start_cash = start_cash
        self.min_bet = min_bet
        self.players = players
        
    def getStartCash(self):
        return self.start_cash
    
    def setStartCash(self, value):
        if isinstance(value, int) and value > self.min_bet:
            self.start_cash = value
            message = f'The starting cash was updated sucessfully to {value}!'
        else:
            message = 'Make sure to select a number greater than the minimum bet!'
        return message
    
    def getMinBet(self):
        return self.min_bet
        
    def setMinBet(self, value):
        if isinstance(value, int) and value < self.start_cash and value >= 0:
            self.min_bet = value
            message = f'The minimum bet was updated successfully to {value}!'
        else:
            message = 'Make sure to select a nonnegative number less than the starting cash.'
        return message
    
    def getPlayers(self):
        return self.players
        
    def setPlayers(self, value):
        if isinstance(value, int) and value >= 1:
            self.players = value
            message = f'You\'re ready to play with {value} players!'
        else:
            message = 'You\'ll need at least 1 player to try and beat the dealer!'
        return message
    
class Blackjack:
    def __init__(self, settings=Settings()):
        self.settings = settings
        
    def changeSettings(self):
        to_change = ''
        message = ''
        while to_change != 'done':
#             clear_output()
            self.displaySettingsMenu(message)
            to_change = input('Which setting would you like to change? Type \'DONE\' to go back ').lower()
            
            if to_change == '1' or to_change == 'cash' or to_change == 'starting cash':
                value = int(input('Please enter a new value for the starting cash. '))
                message = self.settings.setStartCash(value)
                
            elif to_change == '2' or to_change == 'bet' or to_change == 'minimum bet':
                value = int(input('Please enter a new value for the minimum bet. '))
                message = self.settings.setMinBet(value)
                
            elif to_change == '3' or to_change == 'players' or to_change == 'number of players':
                value = int(input('Please enter a new value for the number of players. '))
                message = self.settings.setPlayers(value)
                
            elif to_change == 'done':
                continue
                
            else:
                message = 'Your input was not recognized'
        
        
    def displaySettingsMenu(self, message=''):
        print('{:^35}'.format('SETTINGS'))
        print('=' * 35)
        print('{:<20}{:>14}'.format('1. Starting Cash:', self.settings.getStartCash()))
        print('{:<20}{:>14}'.format('2. Minimum Bet:', self.settings.getMinBet()))
        print('{:<20}{:>14}'.format('3. Number of Players', self.settings.getPlayers()))
        print('\n',message)
        
    def instantiateDeck(self):
        deck = set([])
        suits = set(['spades', 'hearts', 'diamonds', 'clubs'])
        values = set([2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'])
        for value in values:
            for suit in suits:
                for i in range(7):
                    deck.add(Card(value, suit))
        return deck
    
    def instantiatePlayers(self):
        dealer = Player('Dealer', dealer=True)
        players = [dealer]
        for i in range(self.settings.getPlayers()):
            players.append(Player(input(f'Player{i+1}, what is your name? ').title()))
        return players
    
    def generateCard(self, deck):
        card = choice(tuple(deck))
        deck.remove(card)
        print('gen ' + card.getName())
        return card
    
    def dealHands(self, players, deck):
        for player in players:
            if player.dealer:
                downCard = self.generateCard(deck)
                downCard.setFaceDown()
                player.addCard(downCard)
                player.addCard(self.generateCard(deck))
                print('if ' + player.name + str(player.getHand()))
            
            else:
                player.addCard(self.generateCard(deck))
                player.addCard(self.generateCard(deck))
                print('else ' + player.name + str(player.getHand()))
                
    def placeBets(self, players):
        message = ''
        bets = {0 : 0}
        for i in range(1, len(players)):
            bets[i] = None
            while bets[i] == None:
#                 clear_output()
                self.displayMessage(message)
                bet = input(f'{players[i].getName()}, how much would you like to bet? ')
                try:
                    if int(bet) >= self.settings.getMinBet():
                        bets[i] = int(bet)
                    else:
                        message = f'Not at this table! The minimum bet is {self.settings.getMinBet()}.'
                except:
                    message = 'Your bet has to be a number!'
        return bets
    
    def playHand(self, player, deck, bet, split_count=0):
        '''
        This is the complicated one:
        playHand(player, deck, bet, split_count=0) ... Its typing is as follows:
        function(Player, set(Cards), 0 <= int, 0<= int <= 3)
        return [[int, int, boolean, boolean], [], ...] 
        This list will have up to 4 elements (number of split hands)
        '''
        hand_info = []
        
        # First, ask if they'd like to split
        cards = list(player.getHand())
        print('Start of PlayHand' + cards)
        card_values = list(map(lambda card: card.getValue(), cards))
        if card_values[0] == card_values[1] and player.getCash() >= bet*2 and split_count <= 3:
            valid_input = False
            while not valid_input:
                self.displayMessage(message)
                split = input('Would you like to split? ').lower
                if split == 'y' or split == 'yes':
                    valid_input = True
                    split_count += 1
                    for card in cards:
                        player.clearHand()
                        player.addCard(card)
                        player.addCard(self.generateCard(deck))
                        hand_info.append(self.playHand(player, deck, bet, split_count)[0])
                    return hand_info
                    
                elif split == 'n' or split == 'no':
                    valid_input = True
                else:
                    message = 'Please answer with yes or no.'
                    
        # Check for blackjack
        blackjack = False
        hand_value, bust = player.checkHandValue()
        if hand_value == 21:
            blackjack = True
            message = f'Woohoo, {player.getName()}! Blackjack!!'
            
        # Offer to double down
        doubled_down = False
        if blackjack == False and player.getCash() >= bet*2 and split_count == 0:
            message = ''
            valid_input = False
            while not valid_input:
                self.displayMessage(message)
                double = input('Would you like to double down? ').lower()
                if double == 'y' or double == 'yes':
                    valid_input = True
                    doubled_down = True
                    bet *= 2
                    player.addCard(self.generateCard(deck))
                    hand_value, bust = player.checkHandValue()
                    hand_info.append([hand_value, bet, bust, blackjack])
                    return hand_info
                    
                elif double == 'n' or double == 'no':
                    valid_input = True
                else:
                    message = 'Please answer with yes or no.'
        
        # Lastly, standard hitting
        while not bust and not blackjack and not doubled_down:
            valid_input = False   
            while not valid_input:
                move = input('Hit or stay?').lower()
                if move == 'stay':
                    valid_input = True
                    hand_info.append([hand_value, bet, bust, blackjack])
                    return hand_info
                elif move == 'hit':
                    valid_input = True
                    player.addCard(self.generateCard(deck))
                    hand_value, bust = player.checkHandValue()
                else:
                    message = 'Please answer with hit or stay.'
                    
        hand_info.append([hand_value, bet, bust, blackjack])          
        return hand_info
    
    def dealerPlays(self, player, deck):
        dealer_hand_info = list(player.checkHandValue()).append(False)
        if dealer_hand_info[0] == 21:
            dealer_hand_info[2] = True
        while dealer_hand_info[0] <= 16:
            player.addCard(self.generateCard(deck))
            dealer_hand_info[0], dealer_hand_info[1] = player.checkHandValue()
        return dealer_hand_info
                
                
    def playRound(self, players, deck):
        bets = self.placeBets(players)
        self.dealHands(players, deck)
        round_results = {}
        turn_counter = 1
        while turn_counter < len(players):
#             clear_output()
            self.displayTable(players, turn_counter)
            round_results[turn_counter] = self.playHand(players[turn_counter], deck, bets[turn_counter])
            turn_counter += 1
        turn_counter = 0
        round_results[0] = self.dealerPlays()
        
        # Tabulate outcomes of bets
        for k, v in round_results.items():
            if k == 0:
                continue
            else:
                for hand in v:
                    
                    # Busted
                    if hand[2] == True:
                        players[k].setCash(-hand[1])
                        
                    # Blackjack    
                    elif hand[3] == True:
                        
                        # Dealer got blackjack
                        if round_results[0][2] == True:
                            continue
                        else:
                            players[k].setCash(hand[1])
                    
                    # No bust or blackjack
                    else:
                        
                        # Dealer busted
                        if round_result[0][1] == True:
                            players[k].setCash(hand[1])
                            
                        # Dealer got blackjack    
                        elif round_result[0][2] == True:
                            players[k].setCash(-hand[1])
                            
                        # Lastly, comparing sums    
                        else:
                            if hand[0] > round_result[0][0]:
                                players[k].setCash(hand[1])
                                
                            elif hand[0] == round_result[0][0]:
                                continue
                                
                            else:
                                players[k].setCash(-hand[1])
                                
        

    def playGame(self):
        valid_input = False
        while not valid_input:
#             clear_output()
            user_input = input('Welcome. You may \'PLAY\' blackjack, \'CHANGE\' settings, or \'QUIT\'. ').lower()
            
            if user_input == 'play':
                play_again = True
                deck = self.instantiateDeck()
                players = self.instantiatePlayers()
                while play_again:
                    if len(deck) < 182:
                        deck = self.instantiateDeck()
                    self.playRound(players, deck)
                    while not valid_input:
                        keep_playing = input('Would you like to \'PLAY\' another round, or go back to the \'MENU\'? ').lower()
                        if keep_playing == 'play':
                            valid_input = True
                            continue
                        elif keep_playing == 'menu':
                            valid_input = True
                            play_again = False
                        else:
                            message = 'Your input was not recognized'
                
            elif user_input == 'change':
                valid_input = True
                self.changeSettings()
            
            elif user_input == 'quit':
                valid_input = True
                global terminate
                terminate = True
                break
                
            else:
                message = 'Your input was not recognized'
            
    
    def displayTable(self, players=[], turn_counter=0):
        print('BLACKJACK')
        for player in players:
            print(f'{player.getName()}: ${player.getCash()} \n Hand: ')
            for card in player.getHand():
                if not card.face_up:
                    print('Hidden')
                else:
                    print(card.getName())
        if turn_counter > 0:   
            print(f'{players[turn_counter].getName()}, it\'s your turn!')
            
    def displayMessage(self, message=''):
        print('\n\t' + message)
            

terminate = False
while not terminate:
    game = Blackjack()
    game.playGame()

