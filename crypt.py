from cards import *
from player import *
import numpy as np

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

    def get_current_bid(self, place):
        current_bid = 0
        for dice in self.board[place]['servants']:
            current_bid += dice.value
        return current_bid

    def get_input_state(self):
        return np.array([
        self.board[1]['card'].coinvalue, self.board[1]['card'].type, self.get_current_bid(1), 
        self.board[2]['card'].coinvalue, self.board[2]['card'].type, self.get_current_bid(2),
        self.board[3]['card'].type, self.get_current_bid(3),
        self.players[0].nr_remains(), self.players[0].nr_idols(), self.players[0].nr_jewelry(),
        self.players[0].nr_manuscripts(), self.players[0].nr_pottery(), self.players[0].nr_tapestries(),
        self.players[0].nr_servants_available(), self.players[0].score,
        self.players[1].nr_remains(), self.players[1].nr_idols(), self.players[1].nr_jewelry(),
        self.players[1].nr_manuscripts(), self.players[1].nr_pottery(), self.players[1].nr_tapestries(),
        self.players[1].nr_servants_available(), self.players[1].score,
        self.turnsLeft
    ])

    def countServants(self):
        self.players[0].score += self.players[0].nr_servants_available()
        self.players[1].score += self.players[1].nr_servants_available()

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




    def get_total_score(self):
        player1 = self.players[0]
        player2 = self.players[1]

        p1_score = 0
        p2_score = 0

        for i in range(1, 3):
            p1_score += self.collectors[i].get_score(player1)
            p2_score += self.collectors[i].get_score(player2)

        for i in range(3, 6):
            p1_score += self.collectors[i].get_score(player1)
            p2_score += self.collectors[i].get_score(player2)
        man1_score, man2_score = self.collectors[6].get_score(player1, player2)
        p1_score += man1_score
        p2_score += man2_score

        return p1_score, p2_score


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
            self.players[playerNr].exhaustAServant()
            return
        else:
            self.players[playerNr].recoverServantFromCard()

    def rollWithAction(self, playerNr, servant):
        roll = servant.roll()
        if roll < servant.effort_value:
            newRoll = self.collectors[2].useCard(self.players[playerNr])
            if newRoll < servant.effort_value:
                self.players[playerNr].exhaustAServant()
                return
            else:
                self.players[playerNr].recoverServantFromCard()
        else:
            self.players[playerNr].recoverServantFromCard()
    
    def collectTreasure(self, playerNr, place):
        card = self.board[place]['card']
        if card.face_up:
            card.turnCard()
        self.players[playerNr].addTreasure(card)


    def addServant2Card(self, playerNr, place, servants, value):
        
        otherPlayerNr = 0 if playerNr == 1 else 1
        if not len(self.board[place]['servants']) == 0:
            nr_servants_on_card = len(self.board[place]['servants'])
            for i in range(nr_servants_on_card):
                self.players[otherPlayerNr].bump_off_servant()
            self.board[place]['servants'].clear()

        for i in range(servants):
            servant = self.players[playerNr].useServant(value)
            servant.setEffort(value)
            self.board[place]['servants'].append(servant)

    def printTrainScore(self):
        if self.players[0].score > self.players[1].score:
            winner = 'Model'
        elif self.players[0].score < self.players[1].score:
            winner = 'Random'
        else:
            winner = 'Draw'
        print('Model Score: ', self.players[0].score, ' - ', 'Random AI Score: ', self.players[1].score, ' - ', 'Winner: ', winner)