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


    def Action(self, playerNr):
        if self.players[playerNr].servants:
            self.hasServants(playerNr)
        else:
            self.noServants(playerNr)

    def hasServants(self, playerNr):
        print(self.players[playerNr].color, 'turn')
        print('1: Claim a card')
        print('2: Recover all servants')
        print('3: Use Treasures')
        action = input('Choose an action: ')
        if action == '1':
            self.claimCard(playerNr)
            if self.players[playerNr].servants:
                self.claimAgain(playerNr)
        elif action == '2':
            self.players[playerNr].recoverServants()
            #end turn
        elif action == '3':
            #end turn
            pass
        else:
            print('Invalid input')
            self.hasServants(playerNr)

    def lastAction(self, playerNr):
        print(self.players[playerNr].color, 'turn')
        print('')
        print('1: Claim a card')
        print('2: Use Treasures')
        print('-: End turn')
        action = input('Choose an action: ')
        if action == '1':
            self.claimCard(playerNr)
        elif action == '2':
            #end turn
            pass
        elif action == '-':
            #pass turn
            pass
        else:
            print('Invalid input')
            self.lastAction(playerNr)

    def noServants(self, playerNr):
        print(self.players[playerNr].color, 'turn')
        print('1: Recover all servants')
        print('2: Use Treasures')
        action = input('Choose an action: ')
        if action == '1':
            self.players[playerNr].recoverServants()
            #end turn
        elif action == '2':
            #end turn
            pass
        else:
            print('Invalid input')
            self.noServants(playerNr)

    def claimAgain(self, playerNr):
        print('')
        action = input('1: Claim again   2: End turn -> ')
        print('')
        if action == '1':
            self.claimCard(playerNr)
        elif action == '2':
            pass
        else:
            print('Invalid input')
            self.claimAgain(playerNr)

        if self.players[playerNr].servants:
            self.claimAgain(playerNr)
        else:
            pass


    def claimCard(self, playerNr):
        #### Check so place is between 1 and 3
        place = int(input('Choose a place: '))
        if place < 1 or place > 3:
            print('Invalid input')
            self.claimCard(playerNr)

        #Check if player has enough servants to use
        servants = int(input('Choose a number of servants: '))
        if servants > len(self.players[playerNr].servants):
            print('You do not have enough servants to do that')
            self.claimCard(playerNr)

        #### Check so value is between 1 and 6
        value = int(input('Choose a value: '))
        if value < 1 or value > 6:
            print('Invalid input')
            self.claimCard(playerNr)

        #Check if card servants is not empty
        if self.board[place]['servants']:
            current_bid = 0
            for dice in self.board[place]['servants']:
                current_bid += dice.value
            #Check if player can outbid current bid
            if current_bid > value*servants:
                print('You need to bid higher')
                self.claimCard(playerNr)
            else:
                # Push away current servants
                otherPlayerNr = 0 if playerNr == 1 else 1
                for i in range(len(self.board[place]['servants'])):
                    self.board[place]['servants'].pop()
                    self.players[otherPlayerNr].recoverSingleServant()

                self.addServant2Card(playerNr, place, servants, value)
        else:
            self.addServant2Card(playerNr, place, servants, value)
        
        self.printBoard()

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
        


crypt = Crypt()
crypt.revealphase()
crypt.claimphase()






