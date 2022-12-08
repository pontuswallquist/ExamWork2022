from cards import *
from player import *
import numpy as np
from rich.console import Console

class Crypt:

    def __init__(self):
        # Initalize deck of treasure cards
        self.deck = []
        for type in range(1, 7):
            for value in range(1, 5):
                self.deck.append(TreasureCard(type, value))
        random.shuffle(self.deck)

        # For rendering the game
        self.console = Console()
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

        #self.exhaustedServants = []
        
        #Initialize board
        self.board = {
            1: {'card': None, 'servants': [] },
            2: {'card': None, 'servants': [] },
            3: {'card': None, 'servants': [] }
        }
        self.turnsLeft = 8

    def reset(self):
        del self.players
        del self.collectors
        del self.board
        del self.deck
        del self.turnsLeft
        del self.console
        self.__init__()

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
        self.players[0].nr_servants_available(), self.players[0].score + self.players[0].nr_servants_available(),
        self.players[1].nr_remains(), self.players[1].nr_idols(), self.players[1].nr_jewelry(),
        self.players[1].nr_manuscripts(), self.players[1].nr_pottery(), self.players[1].nr_tapestries(),
        self.players[1].nr_servants_available(), self.players[1].score + self.players[1].nr_servants_available(),
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
        bumped_off = False
        otherPlayerNr = 0 if playerNr == 1 else 1
        if not len(self.board[place]['servants']) == 0:
            nr_servants_on_card = len(self.board[place]['servants'])
            for i in range(nr_servants_on_card):
                self.players[otherPlayerNr].bump_off_servant()
            self.board[place]['servants'].clear()
            bumped_off = True

        for i in range(servants):
            servant = self.players[playerNr].useServant(value)
            servant.setEffort(value) #servant was None
            self.board[place]['servants'].append(servant)

        return bumped_off

    def printTrainScore(self):
        if self.players[0].score > self.players[1].score:
            winner = 'Model'
        elif self.players[0].score < self.players[1].score:
            winner = 'Random'
        else:
            winner = 'Draw'
        print('Model Score: ', self.players[0].score, ' - ', 'Random AI Score: ', self.players[1].score, ' - ', 'Winner: ', winner)

    def revealPhase(self):
        self.turnsLeft -= 1
        self.updateNewBoard(1)
        self.updateNewBoard(2)
        self.updateNewBoard(3)


    def claimPhase(self, enemy_agent, train_agent, train, log):

        # Penalty for missing servants
        penalty = 3 * (self.players[1].nr_servants_available() - 3)
    
        if self.players[0].hasTorch():
            turn = 0
        else:
            turn = 1

        p0_played = False
        p1_played = False

        phase_over = False
        while not phase_over:

            if turn == 3 and self.players[0].hasTorch():
                break
            elif turn == 4 and self.players[1].hasTorch():
                break

        #Model to train against
            if turn % 2 == 0:
                list_of_actions, actionspace = self.Actions(0, turn, p0_played)
                if len(list_of_actions) == 0:
                    turn += 1
                    continue
            
            #Make sure we only train one agent against the other
                action, action_id = enemy_agent.step(self.get_input_state(), list_of_actions, actionspace, False)
                #action = random.choice(list_of_actions)

                if train is True or log is True:
                    curr__input_state = copy.deepcopy(self.get_input_state())
                
                reward = self.ResultOfAction(0, action)
                p0_played = True
            
                if log is True:
                    self.console.print(curr__input_state.tolist(), action, reward, sep='\n', justify='center', style='bold red')
                #log_action(curr__input_state, action, 0)

                if turn == 2 and self.players[0].hasTorch() and p0_played and p1_played:
                    phase_over = True

                if action == 'Recover':
                    turn += 1
                    continue
    ##################################################################################
        #Model to train
            elif turn % 2 == 1:   
                list_of_actions, actionspace = self.Actions(1, turn, p1_played)
                if len(list_of_actions) == 0:
                    turn += 1
                    continue

                action, action_id = train_agent.step(self.get_input_state(), list_of_actions, actionspace, train)

                if train is True or log is True:
                    curr__input_state = copy.deepcopy(self.get_input_state())

                reward = self.ResultOfAction(1, action)
                p1_played = True

                if turn == 1:
                    reward += penalty

                if log is True:
                    self.console.print(curr__input_state.tolist(), action, reward, sep='\n', justify='center', style='bold blue')
                    
                # call Remember with the state before action, action, reward, state after action, done
                if train is True:
                    done, reward = self.checkIfDone(1, action, reward, turn, p0_played)
                    train_agent.remember(curr__input_state, action_id, reward, self.get_input_state(), done)
                    train_agent.replay()
                    
                    if done:
                        #if train is True:
                        #    train_agent.target_train()
                        turn += 1
                        continue

                if turn == 3 and self.players[1].hasTorch() and p0_played and p1_played:
                    phase_over = True
                
                if action == 'Recover':
                    turn += 1                
                    continue

    def collectPhase(self):

        if self.players[0].ifAllServantsPushedOut():
            self.players[0].recoverAllExhaustedServants()
        elif self.players[1].ifAllServantsPushedOut():
            self.players[1].recoverAllExhaustedServants()
        

        self.collectCards()
        self.players[0].score = 0
        self.players[1].score = 0
        self.players[0].score, self.players[1].score = self.get_total_score()
        
        servants_to_roll = self.mergeServants()
        for servant in servants_to_roll:
            if servant.color == 'Red':
                if self.players[0].hasIdol():
                    self.rollWithAction(0, servant)
                else:
                    self.rollWithoutAction(0, servant)
            elif servant.color == 'Blue':
                if self.players[1].hasIdol():
                    self.rollWithAction(1, servant)
                else:
                    self.rollWithoutAction(1, servant)

    def passTorchPhase(self, game_over):
        if not self.deck:
            # reset score and count score
            self.players[0].score = 0
            self.players[1].score = 0
            self.countBonus()
            self.calculateCollectionScore()
            self.countServants()
            game_over = True
        else:
            self.players[0].torch = not self.players[0].torch
            self.players[1].torch = not self.players[1].torch
            game_over = False
        return game_over

    def checkIfDone(self, playerNr, action, reward, turn, hasPlayed):
        otherPlayerNr = 0 if playerNr == 1 else 1

        self.players[0].score = 0
        self.players[1].score = 0
        self.players[0].score, self.players[1].score  = self.get_total_score()


        if self.turnsLeft == 0 and not self.hasAvailableActions(playerNr, turn, hasPlayed) or self.turnsLeft == 0 and action == 'Recover':
            done = True
            reward = 10 * (self.players[playerNr].score - self.players[otherPlayerNr].score)
        else:
            done = False
        
        return done, reward

    def hasAvailableActions(self, playerNr, turn, hasPlayed):
        action_list, _ = self.Actions(playerNr, turn, hasPlayed)
        if len(action_list) == 0:
            return False
        else:
            return True

    

        
    def ActiontoIndex(self, place, servant, value):
        servantIndex = servant - 1
        valueIndex = value - 1
        rowIndex = place
        columnIndex = servantIndex * 6 + valueIndex
        return rowIndex, columnIndex

    def makeActionSpace1D(self, actionspace):
        actionspace1D = []
        actionspace1D.extend(actionspace[0])
        actionspace1D.extend(actionspace[1])
        actionspace1D.extend(actionspace[2])
        actionspace1D.extend(actionspace[3])
        return actionspace1D


    def Actions(self, playerNr, turn, hasPlayed):
        actionspace = [
        [0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        actions = []

        servants_available = self.players[playerNr].nr_servants_available()

        if (playerNr == 0 and turn == 0 and not hasPlayed) or (playerNr == 1 and turn == 1 and not hasPlayed):
            if self.players[playerNr].hasExhaustedServants():
                actionspace[0][0] = 1
                actions.append('Recover')
            
        # Servant needs to be exhausted to be used by remains card or recover
        if self.players[playerNr].hasExhaustedServants():
            if self.players[playerNr].hasRemainsCards():
                    actionspace[0][1] = 1
                    actions.append('useRemains')

        if servants_available == 0:
            return actions, actionspace
        
        for place in self.board.keys():
            if len(self.board[place]['servants']) == 0:
                for servant in range(1, servants_available + 1):
                    for value in range(1,7):
                        # If action is valid, add it to the list of actions and add it to the action space
                        rowIndex, columnIndex = self.ActiontoIndex(place, servant, value)
                        actionspace[rowIndex][columnIndex] = 1
                        actions.append(str(place) + '-' + str(servant) + '-' + str(value))
            else:
                #If place is occupied, check if player already has a servant there
                if self.board[place]['servants'][0].color == self.players[playerNr].color:
                    continue
                #If there are servants on the board, check if the player can outbid the current bid
                current_bid = 0
                for dice in self.board[place]['servants']:
                    current_bid += dice.value
                for servant in range(1, servants_available + 1):
                    for value in range(1,7):
                        if current_bid < value*servant:
                            rowIndex, columnIndex = self.ActiontoIndex(place, servant, value)
                            actionspace[rowIndex][columnIndex] = 1
                            actions.append(str(place) + '-' + str(servant) + '-' + str(value))

        return actions, actionspace

    def ResultOfAction(self, playerNr, action):
        reward = 0
        if action == 'Recover':
            if self.players[playerNr].nr_servants_available() == 0:
                reward = -5
            elif self.players[playerNr].nr_servants_available() == 1:
                reward = -10
            elif self.players[playerNr].nr_servants_available() == 2:
                reward = -15
            self.players[playerNr].recoverAllExhaustedServants()

        elif action == 'useRemains':
            self.collectors[1].useCard(self.players[playerNr])
            reward = 10
        else:
            bid = action.split('-')

            place = int(bid[0])
            servant = int(bid[1])
            value = int(bid[2])

            
            bumped_off = self.addServant2Card(playerNr, place, servant, value)
            

            card = self.board[place]['card']

            #subtract potential score for the player who was bumped off card
            otherPlayerNr = 1 if playerNr == 0 else 0
            if bumped_off:
                if card.type == 6:
                    self.players[otherPlayerNr].score -= self.collectors[card.type].potentialValue(card, self.players[otherPlayerNr], self.players[playerNr])
                else:
                    self.players[otherPlayerNr].score -= self.collectors[card.type].potentialValue(card, self.players[playerNr])

            #Add potential score for the player who owns the card
            if card.type == 6:
                self.players[playerNr].score += self.collectors[card.type].potentialValue(card, self.players[playerNr], self.players[otherPlayerNr])
            else:
                self.players[playerNr].score += self.collectors[card.type].potentialValue(card, self.players[playerNr])
            
            
            ## With just the score as reward, the agent will always try to get the highest score possible
            reward = self.players[playerNr].score + self.players[playerNr].nr_servants_available()

            #Try with penalty for using servants
            
        return reward

    def ReducePossibleActions(self, actionspace, actions):
        actionspace1d = self.makeActionSpace1D(actionspace)
        for i in range(len(actionspace1d)):
            actions[i] = actions[i] * actionspace1d[i]
        return actions

    def playGame(self, enemy_agent, train_agent, train, log):
        game_over = False
        while not game_over:
            self.revealPhase()
            self.claimPhase(enemy_agent, train_agent, train, log)
            self.collectPhase()
            game_over = self.passTorchPhase(game_over)