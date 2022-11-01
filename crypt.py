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

        
        #Initialize board
        self.board = {
            1: {'card': None, 1: 0, 2: 0, 3: 0},
            2: {'card': None, 1: 0, 2: 0, 3: 0},
            3: {'card': None, 1: 0, 2: 0, 3: 0}
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
    
    def sumofservants(self, place):
        return self.board[place][1].value + self.board[place][2].value + self.board[place][3].value


    def checkOpenCard(self, place):
        return self.board[place][1] == 0 and self.board[place][2] == 0 and self.board[place][3] == 0
        

    def printBoard(self):
        print('1:', self.board[1]['card'])
        print('2:', self.board[2]['card'])
        print('3:', self.board[3]['card'])
        

player1 = Player()
crypt = Crypt()
crypt.revealphase()




