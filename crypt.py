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
        for place in self.board:
            for servant in self.board[place]:
                if color in servant:
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

    def printScore(self):
        print('GAME OVER!')
        print('Red Treasures: ', self.players[0].collection)
        print('Red servants: ', self.players[0].servants)
        print('Red score: ', self.players[0].score)
        print('')
        print('Blue Treasures: ', self.players[1].collection)
        print('Blue servants: ', self.players[1].servants)
        print('Blue score: ', self.players[1].score)


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
        self.collectCards()
        self.rollDices()

    def printRoundInfo(self, playerNr):
        print(self.players[playerNr].color, 'turn!')
        print('Servants available:', self.players[playerNr].servants)
        print('Treasures collected:', self.players[playerNr].collection)
        print('')

    def collectCards(self):
        for place in range(1, 4):
            for servant in self.board[place]['servants']:
                if servant.color == 'Red':
                    self.collectTreasure(0, place)
                else:
                    self.collectTreasure(1, place)

    ########## rework in to smaller function for a particular player
    def rollDices(self):
        print('====================================================')
        for place in range(1,4):
            for servant in self.board[place]['servants']:
                roll = servant.roll()
                if servant.color == 'Red':
                    if roll >= servant.effort_value:
                        print('Red player rolls', roll)
                        self.players[0].recoverSingleServant()
                    else:
                        print('Red player rolls', roll)
                        if self.players[0].hasIdol():
                            print(self.players[0].color, 'player: ','Roll again? 1: Yes, 2: No')
                            answer = self.get_input(1,2)
                            if answer == '1':
                                roll = self.collectors[2].useCard(self.players[0])
                                if roll >= servant.effort_value: 
                                    print('Red player rolls', roll)
                                    self.players[0].recoverSingleServant()
                                else:
                                    print('Red player rolls', roll, 'and servant is exhausted')
                            else:
                                print('Red servant is exhausted')
                        else:
                            print('Red player rolls', roll, 'and servant is exhausted')
                else:
                    if roll >= servant.effort_value:
                        print('Blue player rolls', roll)
                        self.players[1].recoverSingleServant()
                    else:
                        print('Blue player rolls', roll)
                        if self.players[1].hasIdol():
                            print(self.players[1].color, 'player: ','Roll again? 1: Yes, 2: No')
                            answer = self.get_input(1,2)
                            if answer == '1':
                                roll = self.collectors[2].useCard(self.players[1])
                                if roll >= servant.effort_value:
                                    print('Blue player rolls', roll)
                                    self.players[1].recoverSingleServant()
                                else:
                                    print('Blue player rolls', roll, 'and servant is exhausted')
                            else:
                                print('Blue servant is exhausted')
                        else:
                            print('Blue player rolls', roll, 'and servant is exhausted')
        print('====================================================')
        

    def collectTreasure(self, playerNr, place):
        card = self.board[place]['card']
        if card.face_up:
            card.turnCard()
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
        print('3: Use Remains cards to recover a servant')
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
            if self.players[playerNr].hasRemains():
                self.collectors[1].useCard(self.players[playerNr])
                self.lastAction(playerNr)
            return


    def lastAction(self, playerNr):
        if not self.players[playerNr].servants:
            return
        self.printRoundInfo(playerNr)
        print('1: Claim a card')
        print('2: Use Treasures')
        print('3: End turn')
        action = self.get_input(1,3)
        if action == '1':
            self.claimCard(playerNr)
        elif action == '2':
            pass
        elif action == '3':
            pass
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





