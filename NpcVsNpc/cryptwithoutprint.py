from cards import *
from playerwithoutprint import *

class Crypt:

    def __init__(self):
        # Initalize deck of treasure cards
        self.deck = []
        for type in range(1, 7):
            for value in range(1, 5):
                self.deck.append(TreasureCard(type, value))
        random.shuffle(self.deck)

        # Initialize Collector cards
        self.collectors = {
            1: RemainsCollector(),
            2: IdolCollector(),
            3: JewelryCollector(),
            4: ManuscriptCollector(),
            5: PotteryCollector(),
            6: TapestryCollector()
        }

        # Initialize players
        self.players = [Player('Red', True), Player('Blue')]
        
        #Initialize board
        self.board = {
            1: {'card': None, 'servants': [] },
            2: {'card': None, 'servants': [] },
            3: {'card': None, 'servants': [] }
        }
        self.turnsLeft = 8

    def countServants(self):
        self.players[0].score += len(self.players[0].servants)
        self.players[1].score += len(self.players[1].servants)

    def countBonus(self):
        self.players[0].turnAllCards()
        self.players[1].turnAllCards()
        for i in range(3,6):
            self.collectors[i].useCard(self.players[0])
            self.collectors[i].useCard(self.players[1])
        self.collectors[6].useCard(self.players[0], self.players[1])
    
    def anyServants(self, color):
        for place in self.board.keys():
            for servant in self.board[place]['servants']:
                if servant.color == color:
                    return True
        return False

    def mergeServants(self):
        #merge servants lists to one list
        merged = []
        for place in self.board:
            merged.extend(self.board[place]['servants'])
        return merged

    def calculateCollectionScore(self):
        #Player 1 score
        for card in self.players[0].collection:
            self.players[0].score += card.coinvalue
        #Player 2 score
        for card in self.players[1].collection:
            self.players[1].score += card.coinvalue


    def updateNewBoard(self, place):
        card = self.deck.pop()
        if place <= 2:
            card.turnCard()
        self.board[place]['card'] = card
        self.board[place]['servants'] = []


    def collectCards(self):
        for place in range(1, 4):
            for servant in self.board[place]['servants']:
                if servant.color == 'Red':
                    self.collectTreasure(0, place)
                    break
                elif servant.color == 'Blue':
                    self.collectTreasure(1, place)
                    break

    def rollWithoutAction(self, playerNr, servant): 
        roll = servant.roll()
        if roll < servant.effort_value:
            return
        else:
            self.players[playerNr].recoverSingleServant()

    def rollWithAction(self, playerNr, servant):
        roll = servant.roll()
        if roll < servant.effort_value:
            newRoll = self.collectors[2].useCard(self.players[playerNr])
            if newRoll < servant.effort_value:
                return
            else:
                self.players[playerNr].recoverSingleServant()
        else:
            self.players[playerNr].recoverSingleServant()
    
    def collectTreasure(self, playerNr, place):
        card = self.board[place]['card']
        if card.face_up:
            card.turnCard()
        self.players[playerNr].addTreasure(card)


    def addServant2Card(self, playerNr, place, servants, value):
        otherPlayerNr = 0 if playerNr == 1 else 1
        if not len(self.board[place]['servants']) == 0:
            for i in range(len(self.board[place]['servants'])):
                self.board[place]['servants'].pop()
                self.players[otherPlayerNr].recoverSingleServant()

        for i in range(servants):
            servant = self.players[playerNr].useServant(value)
            servant.setEffort(value)
            self.board[place]['servants'].append(servant)
