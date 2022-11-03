from cards import *
from player import *

class Crypt:

    def __init__(self):
        # Initalize deck of treasure cards
        self.deck = []
        for type in range(1, 7):
            for value in range(1, 5):
                self.deck.append(TreasureCard(type, value))
        random.shuffle(self.deck)

        # Initialize players
        self.players = [Player('Red', True), Player('Blue')]
        
        #Initialize board
        self.board = {
            1: {'card': None, 'servants': [] },
            2: {'card': None, 'servants': [] },
            3: {'card': None, 'servants': [] }
        }
        self.turnsLeft = 8
    
    def passTorchphase(self, loop):
        if not self.deck:
            self.calcScore()
            self.printScore()
            loop = False
        else:
            self.players[0].torch = not self.players[0].torch
            self.players[1].torch = not self.players[1].torch
            loop = True
        return loop

    def calcScore(self):
        p1_score = 0
        for card in self.players[0].collection:
            p1_score += card.coinvalue
        self.players[0].score = p1_score

        p2_score = 0
        for card in self.players[1].collection:
            p2_score += card.coinvalue
        self.players[1].score = p2_score

    def printScore(self):
        print('Red score: ', self.players[0].score)
        print('Blue score: ', self.players[1].score)

    def revealphase(self):
        self.updateNewBoard(1)
        self.updateNewBoard(2)
        self.updateNewBoard(3)
        self.turnsLeft -= 1
        self.printBoard()
    
    def updateNewBoard(self, place):
        card = self.deck.pop()
        if place <= 2:
            card.turnCard()
        self.board[place]['card'] = card
        self.board[place]['servants'] = []

    def claimphase(self):
        if self.players[0].torch:
            self.Action(0)
            self.printBoard()
            self.Action(1)
            self.printBoard()
            self.lastAction(0)
        elif self.players[1].torch:
            self.Action(1)
            self.printBoard()
            self.Action(0)
            self.printBoard()
            self.lastAction(1)

    def collectphase(self):
        self.rollDices()
        self.collectCards()

    def printRoundInfo(self, playerNr):
        print(self.players[playerNr].color, 'turn!')
        print('Servants available:', self.players[playerNr].servants)
        print('')

    def collectCards(self):
        for place in range(1, 4):
            if self.board[place]['servants']:
                if str(self.board[place]['servants'][0]).startswith('Red'): # Maybe change this line
                    self.collectTreasure(0, place)
                else:
                    self.collectTreasure(1, place)

    def rollDices(self):
        print('')
        for place in range(1,4):
            for servant in self.board[place]['servants']:
                roll = servant.roll()
                if servant.color == 'Red':
                    if roll >= servant.effort_value:
                        self.players[0].recoverSingleServant()
                        print('Red player rolls', roll, 'and recovers a servant')
                    else:
                        print('Red player rolls', roll, 'and servant is exhausted')
                else:
                    if roll >= servant.effort_value:
                        self.players[1].recoverSingleServant()
                        print('Blue player rolls', roll, 'and recovers a servant')
                    else:
                        print('Blue player rolls', roll, 'and servant is exhausted')
        

    def collectTreasure(self, playerNr, place):
        card = self.board[place]['card']
        self.players[playerNr].addTreasure(card)

    def Action(self, playerNr):
        if self.players[playerNr].servants:
            self.hasServants(playerNr)
        else:
            self.noServants(playerNr)

    def hasServants(self, playerNr):
        self.printRoundInfo(playerNr)
        print('1: Claim a card')
        print('2: Recover all servants')
        print('3: Use Treasures')
        action = self.get_input(1,3)
        if action == '1':
            self.claimCard(playerNr)
            if self.players[playerNr].servants:
                self.claimAgain(playerNr)
            if self.players[playerNr].servants:
                self.claimAgain(playerNr)
            return
        elif action == '2':
            self.players[playerNr].recoverServants()
            return
        elif action == '3':
            return


    def lastAction(self, playerNr):
        self.printRoundInfo(playerNr)
        print('1: Claim a card')
        print('2: Use Treasures')
        print('3: End turn')
        action = self.get_input(1,3)
        if action == '1':
            if self.players[playerNr].servants:
                self.claimCard(playerNr)
        elif action == '2':
            pass
        elif action == '3':
            pass
        print('===============================================')
        return
        

    def noServants(self, playerNr):
        self.printRoundInfo(playerNr)
        print('1: Recover all servants')
        print('2: Use Treasures')
        action = self.get_input(1,2)
        if action == '1':
            self.players[playerNr].recoverServants()
        elif action == '2':
            return

    def claimAgain(self, playerNr):
        self.printBoard()
        self.printRoundInfo(playerNr)
        action = print('1: Claim again   2: End turn')

        action = self.get_input(1,2)
        if action == '1':
            self.claimCard(playerNr)
        elif action == '2':
            return


    def get_input(self, start, end):
        while True:
            try:
                choice = int(input('\nChoose an action -> '))
                if choice < start or choice > end:
                    raise ValueError
                break
            except ValueError:
                print('Invalid input')
        return str(choice)


    def get_place_servants_value(self, playerNr):
        # Gets input from player
        while True:
            try:
                place = int(input('Choose a place: '))
                if place < 1 or place > 3:
                    raise ValueError
                break
            except ValueError:
                print('Invalid place')
        
        #Check if player has enough servants to use
        while True:
            try:
                servants = int(input('Choose a number of servants: '))
                if servants > len(self.players[playerNr].servants):
                    raise ValueError
                break
            except ValueError:
                print('You don\'t have servants for that')

        # Check so value is between 1 and 6
        while True:
            try:
                value = int(input('Choose a value: '))
                if value < 1 or value > 6:
                    raise ValueError
                break
            except ValueError:
                print('Value must be between 1 and 6')

        return place, servants, value
            

    def claimCard(self, playerNr):
       
       while True:
            try:
                # Get input from player
                place, servants, value = self.get_place_servants_value(playerNr)

                #Check if card servants is not empty
                if self.board[place]['servants']:
                    current_bid = 0
                    for dice in self.board[place]['servants']:
                        current_bid += dice.value
                    #Check if player can outbid current bid
                    if current_bid >= value*servants:
                        raise ValueError
                    # Push away current servants
                    otherPlayerNr = 0 if playerNr == 1 else 1
                    for i in range(len(self.board[place]['servants'])):
                        self.board[place]['servants'].pop()
                        self.players[otherPlayerNr].recoverSingleServant()

                    self.addServant2Card(playerNr, place, servants, value)
                    break
                else:
                    self.addServant2Card(playerNr, place, servants, value)
                    break
            except ValueError:
                print('You need to bid higher, try again')

    def addServant2Card(self, playerNr, place, servants, value):
        for each in range(servants):
                servant = self.players[playerNr].useServant(value)
                servant.setEffort(value)
                self.board[place]['servants'].append(servant)

    def printBoard(self):
        print('')
        print('1:', self.board[1]['card'], '|| Servants:', self.board[1]['servants'])
        print('2:', self.board[2]['card'], '|| Servants:', self.board[2]['servants'])
        print('3:', self.board[3]['card'], '|| Servants:', self.board[3]['servants'])
        print('')
        print(self.turnsLeft, 'turns left')
        print('')
        


crypt = Crypt()
loop = True
while loop:
    crypt.revealphase()
    crypt.claimphase()
    crypt.collectphase()
    loop = crypt.passTorchphase(loop)





