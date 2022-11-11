from cards import *
from playerwithprint import *
from rich.console import Console
from rich.table import Table
from rich import print as rprint
console = Console()

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

    def printScore(self):
        console.print('[bold italic underline green]GAME OVER!', justify='center')
        console.print('[bold blue]Blue:', justify='right')
        console.print('Treasures: ', self.players[1].collection, justify='right')
        console.print('Servants: ', self.players[1].servants, justify='right')
        console.print('Score: ', self.players[1].score, justify='right')
        console.print('[bold red]Red:', justify='left')
        console.print('Treasures: ', self.players[0].collection, justify='left')
        console.print('Servants: ', self.players[0].servants, justify='left')
        console.print('Score: ', self.players[0].score, justify='left')

    def updateNewBoard(self, place):
        card = self.deck.pop()
        if place <= 2:
            card.turnCard()
        self.board[place]['card'] = card
        self.board[place]['servants'] = []

    def printRoundInfo(self, playerNr):
        if self.players[playerNr].color == 'Red':
            console.print(' [bold red]|| Red turn ||', justify='left')
            console.print('[bold red]Servants available:', self.players[playerNr].servants, justify='left')
            console.print('[bold red]Treasures collected:', self.players[playerNr].collection, justify='left')
        else:
            console.print(' [bold blue]|| Blue turn ||', style='bold blue', justify='right')
            console.print('[bold blue]Servants available:', self.players[playerNr].servants, justify='right')
            console.print('[bold blue]Treasures collected:', self.players[playerNr].collection, justify='right')


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
        console.print(self.players[playerNr].color + ' rolled', roll, 'against', servant.effort_value, justify='center')
        if roll < servant.effort_value:
            console.print(self.players[playerNr].color + ' lost a servant', justify='center')
            return
        else:
            self.players[playerNr].recoverSingleServant()

    def rollWithAction(self, playerNr, servant):
        roll = servant.roll()
        if roll < servant.effort_value:
            console.print(self.players[playerNr].color + ' rolled', roll, 'against', servant.effort_value, justify='center')
            newRoll = self.collectors[2].useCard(self.players[playerNr])
            console.print(self.players[playerNr].color + ' used Idol card to re-roll', newRoll, 'against', servant.effort_value, justify='center')
            if newRoll < servant.effort_value:
                console.print(self.players[playerNr].color + ' lost a servant', justify='center')
                return
            else:
                self.players[playerNr].recoverSingleServant()
        else:
            console.print(self.players[playerNr].color + ' rolled', roll, 'against', servant.effort_value, justify='center')
            self.players[playerNr].recoverSingleServant()       

    def collectTreasure(self, playerNr, place):
        card = self.board[place]['card']
        if card.face_up:
            card.turnCard()
        self.players[playerNr].addTreasure(card)

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

    '''
    def printBoard(self):
        console.print('')
        board_table = Table(title='Board')
        board_table.add_column('1', justify='center')
        board_table.add_column('2', justify='center')
        board_table.add_column('3', justify='center')
        board_table.add_row(str(self.board[1]['card']), str(self.board[2]['card']), str(self.board[3]['card']))
        board_table.add_row(str(self.board[1]['servants']), str(self.board[2]['servants']), str(self.board[3]['servants']))
        console.print(board_table, justify='center')
        console.print('')
    '''
    def anyServantsOnPlace(self, color, place):
        for servant in self.board[place]['servants']:
            if servant.color == color:
                return True
        return False

    def printBoard(self):
        console.print('')
        board_table = Table(title='Board')
        if self.anyServantsOnPlace('Red', 1):
            board_table.add_column('1', justify='center', style='bold red')
        elif self.anyServantsOnPlace('Blue', 1):
            board_table.add_column('1', justify='center', style='bold blue')
        else:
            board_table.add_column('1', justify='center')
        if self.anyServantsOnPlace('Red', 2):
            board_table.add_column('2', justify='center', style='bold red')
        elif self.anyServantsOnPlace('Blue', 2):
            board_table.add_column('2', justify='center', style='bold blue')
        else:
            board_table.add_column('2', justify='center')
        if self.anyServantsOnPlace('Red', 3):
            board_table.add_column('3', justify='center', style='bold red')
        elif self.anyServantsOnPlace('Blue', 3):
            board_table.add_column('3', justify='center', style='bold blue')
        else:
            board_table.add_column('3', justify='center')
        board_table.add_row(str(self.board[1]['card']), str(self.board[2]['card']), str(self.board[3]['card']))
        board_table.add_row(str(self.board[1]['servants']), str(self.board[2]['servants']), str(self.board[3]['servants']))
        console.print(board_table, justify='center')
        console.print('')


