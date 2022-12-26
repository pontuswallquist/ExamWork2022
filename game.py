from cards import *
from player import *
import copy
import numpy as np
from rich.console import Console
#import pygame
from time import sleep

colors = {
    'yellow': (255, 200, 0),
    'white': (255, 255, 255)
}

class Crypt:

    def __init__(self, player1, player2):
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
        player1.score = 0
        player2.score = 0
        self.players = [player1, player2]

        #Initialize board
        self.board = {
            1: {'card': None, 'servants': deque([], maxlen=3) },
            2: {'card': None, 'servants': deque([], maxlen=3) },
            3: {'card': None, 'servants': deque([], maxlen=3) }
        }
        self.turnsLeft = 8

    def reset(self):
        self.players[0].reset()
        self.players[1].reset()
        self.__init__(self.players[0], self.players[1])

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
            self.players[playerNr].exhaustAServant(servant)
            #self.console.print(f"{self.players[playerNr].color} player exhausted a servant", justify='center')
            return
        else:
            self.players[playerNr].recoverServantFromCard(servant)

    def rollWithAction(self, playerNr, servant):
        roll = servant.roll()
        if roll < servant.effort_value:
            newRoll = self.collectors[2].useCard(self.players[playerNr])
            if newRoll < servant.effort_value:
                self.players[playerNr].exhaustAServant(servant)
                #self.console.print(f"{self.players[playerNr].color} player exhausted a servant", justify='center')
                return
            else:
                self.players[playerNr].recoverServantFromCard(servant)
        else:
            self.players[playerNr].recoverServantFromCard(servant)
    
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
                servant = self.board[place]['servants'].pop()
                self.players[otherPlayerNr].bump_off_servant(servant)
            self.board[place]['servants'].clear()
            bumped_off = True

        for i in range(servants):
            servant = self.players[playerNr].useServant(value)
            servant.setEffort(value)
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


    def claimPhase(self, train, log):
    
        if self.players[0].hasTorch():
            turn = 0
        else:
            turn = 1

        p0_played = False
        p1_played = False

        phase_over = False
        while not phase_over:
            '''
            if render:
                self.render(screen)
                pygame.display.flip()
                sleep(1)
            '''   
            if turn == 3 and self.players[0].hasTorch():
                break
            elif turn == 4 and self.players[1].hasTorch():
                break

        #Model to train against
            if turn % 2 == 0:
                list_of_actions, actionspace = self.Actions(0, p0_played)
                if len(list_of_actions) == 0:
                    turn += 1
                    continue
            
            
                action, action_id = self.players[0].step(self.get_input_state(), list_of_actions, actionspace, False)

                if train is True or log is True:
                    curr__input_state = copy.deepcopy(self.get_input_state())
                
                reward = self.ResultOfAction(0, action)
                p0_played = True
                p1_played = False
            
                if log is True:
                    self.console.print(curr__input_state.tolist(), f"Turn: {turn}", action, reward, sep='\n', justify='center', style='bold red')
                #log_action(curr__input_state, action, 0)

                if action == 'Recover':
                    turn += 1
                    continue
                
                if turn == 2 and self.players[0].hasTorch():
                    phase_over = True
    ##################################################################################
        #Model to train
            elif turn % 2 == 1:   
                list_of_actions, actionspace = self.Actions(1, p1_played)
                if len(list_of_actions) == 0:
                    turn += 1
                    continue

                action, action_id = self.players[1].step(self.get_input_state(), list_of_actions, actionspace, train)

                if train is True or log is True:
                    curr__input_state = copy.deepcopy(self.get_input_state())

                reward = self.ResultOfAction(1, action)
                p1_played = True
                p0_played = False

                if log is True:
                    self.console.print(curr__input_state.tolist(), f"Turn: {turn}", action, reward, sep='\n', justify='center', style='bold blue')
                    
                # call Remember with the state before action, action, reward, state after action, done
                if train is True:
                    done, reward = self.checkIfDone(1, action, reward, p0_played)
                    self.players[1].remember(curr__input_state, action_id, reward, self.get_input_state(), done)
                    self.players[1].replay()
                    
                    if done:
                        #if train is True:
                        #    train_agent.target_train()
                        turn += 1
                        continue

                
                
                if action == 'Recover':
                    turn += 1               
                    continue

                if turn == 3 and self.players[1].hasTorch():
                    phase_over = True

    def AllServantsPushedOut(self, color):
        #check the board places to see if there is a servant of the given color
        for place in self.board.keys():
            for servant in self.board[place]['servants']:
                if servant.color == color:
                    return False
        return True
        
    def collectPhase(self):

        if self.AllServantsPushedOut('Red'):
            self.players[0].recoverAllExhaustedServants()
        elif self.AllServantsPushedOut('Blue'):
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
            game_over = True
        else:
            self.players[0].torch = not self.players[0].torch
            self.players[1].torch = not self.players[1].torch
            game_over = False
        return game_over

    def checkIfDone(self, playerNr, action, reward, hasPlayed):
        otherPlayerNr = 0 if playerNr == 1 else 1

        self.players[0].score = 0
        self.players[1].score = 0
        self.players[0].score, self.players[1].score  = self.get_total_score()


        if self.turnsLeft == 0 and not self.hasAvailableActions(playerNr, hasPlayed) or self.turnsLeft == 0 and action == 'Recover':
            done = True
            reward = 2 * (self.players[playerNr].score - self.players[otherPlayerNr].score)
        else:
            done = False
        
        return done, reward

    def hasAvailableActions(self, playerNr, hasPlayed):
        action_list, _ = self.Actions(playerNr, hasPlayed)
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


    def Actions(self, playerNr, hasPlayed):
        actionspace = [
        [0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ]
        actions = []

        servants_available = self.players[playerNr].nr_servants_available()

        exhaustedServants = self.players[playerNr].hasExhaustedServants()
        if exhaustedServants and hasPlayed is False:
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
                reward = -10
            elif self.players[playerNr].nr_servants_available() == 1:
                reward = -20
            elif self.players[playerNr].nr_servants_available() == 2:
                reward = -30
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
            otherPlayerNr = 1 if playerNr == 0 else 0
            
            if card.type == 6:
                reward += self.collectors[card.type].potentialValue(card, self.players[playerNr], self.players[otherPlayerNr])
            else:
                reward += self.collectors[card.type].potentialValue(card, self.players[playerNr])
            
            reward += self.players[playerNr].nr_servants_available()
        return reward

    def ReducePossibleActions(self, actionspace, actions):
        actionspace1d = self.makeActionSpace1D(actionspace)
        for i in range(len(actionspace1d)):
            actions[i] = actions[i] * actionspace1d[i]
        return actions

    '''
    def drawCollection(self, screen, color, cards):
        if not cards:
            return
        if color == 'Blue':
            start_x = 420
            start_y = 80
        elif color == 'Red':
            start_x = 460
            start_y = 665
        rects = []
        card_width = 30
        card_height = 40
        spacing = 5
        font = pygame.font.Font("consola.ttf", 24)
        y = start_y
        x = start_x
        for i, card in enumerate(cards):
            if i == 13:
                y = start_y + card_height + spacing
                x = start_x
            rects.append(pygame.Rect(x, y, card_width, card_height))
            pygame.draw.rect(screen, colors['white'], rects[i], 2)
            value_text = font.render(shortcardtypes[card.type], True, colors['yellow'])
            text_width, text_height = value_text.get_size()
            text_x = x + (card_width - text_width) / 2
            text_y = y + (card_height - text_height) / 2
            screen.blit(value_text, (text_x, text_y))
            x = x + card_width + spacing

    def diceNumber(self, color, servant):
        if servant.value <= 1:
            servant_image = pygame.image.load(f'images/{color}One.png')
        elif servant.value == 2:
            servant_image = pygame.image.load(f'images/{color}Two.png')
        elif servant.value == 3:
            servant_image = pygame.image.load(f'images/{color}Three.png')
        elif servant.value == 4:
            servant_image = pygame.image.load(f'images/{color}Four.png')
        elif servant.value == 5:
            servant_image = pygame.image.load(f'images/{color}Five.png')
        elif servant.value == 6:
            servant_image = pygame.image.load(f'images/{color}Six.png')
        return servant_image

    def drawServants(self, screen, color, servants):
        if not servants:
            return
        if color == 'Blue':
            start_x = 90
            start_y = 90
        elif color == 'Red':
            start_x = 1050
            start_y = 670
        dice_width = 60
        dice_height = 60
        spacing = 25

        y = start_y
        x = start_x

        for i, servant in enumerate(servants):
            servant_image = self.diceNumber(color, servant)
            servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
            servant_rect = servant_image.get_rect(topleft=(x, y))
            screen.blit(servant_image, servant_rect)
            x = x + dice_width + spacing

    def drawExhausted(self, screen, color, servants):
        if not servants:
            return
        if color == 'Blue':
            start_x = 1010
            start_y = 90
        elif color == 'Red':
            start_x = 125
            start_y = 670
        dice_width = 60
        dice_height = 60
        spacing = 25

        y = start_y
        x = start_x

        for i, servant in enumerate(servants):
            servant_image = self.diceNumber(color, servant)
            servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
            servant_rect = servant_image.get_rect(topleft=(x, y))
            screen.blit(servant_image, servant_rect)
            
            x = x + dice_width + spacing
    
    def drawBoard(self, screen, board):

        cards = [board[i]['card'] for i in board.keys()]

        card_width, card_height = 200, 250
        card_spacing = 20
        font = pygame.font.Font("consola.ttf", 24)
        # Calculate the total width of the cards
        total_width = card_width * len(cards) + card_spacing * (len(cards) - 1)
        # Calculate the starting x position for the cards
        start_x = 1400 // 2 - total_width // 2


        for i, card in enumerate(cards):
            # Calculate the card position
            x = start_x + i * (card_width + card_spacing)
            y = 800 // 2 - card_height // 2
            # Draw the card outline
            pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height), 2)
            # Draw the card value
            if i < 2:
                value_text = font.render(str(card.coinvalue), True, colors["yellow"])
                value_text_rect = value_text.get_rect()
                value_text_rect.center = (x + card_width // 2, y + card_height // 4)
                screen.blit(value_text, value_text_rect)
            # Draw the card type
            type_text = font.render(cardtypes[card.type], True, colors["white"])
            type_text_rect = type_text.get_rect()
            type_text_rect.center = (x + card_width // 2, y + card_height * 2 // 4)
            screen.blit(type_text, type_text_rect)

        self.drawServantsOnBoard(screen, board[1]['servants'], 1)
        self.drawServantsOnBoard(screen, board[2]['servants'], 2)
        self.drawServantsOnBoard(screen, board[3]['servants'], 3)

    def drawServantsOnBoard(self, screen, servants, card_nr):
        if not servants:
            return
        if card_nr == 1:
            start_x, start_y = 385, 450
        elif card_nr == 2:
            start_x, start_y = 605, 450
        elif card_nr == 3:
            start_x, start_y = 825, 450
        spacing = 5
        dice_width = 60
        dice_height = 60

        x = start_x
        y = start_y

        for i, servant in enumerate(servants):
            servant_image = self.diceNumber(servant.color, servant)
            servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
            servant_rect = servant_image.get_rect(topleft=(x, y))
            screen.blit(servant_image, servant_rect)
            
            x = x + dice_width + spacing

    def drawRecoverButton(self, screen):
        width = 150
        height = 50
        x = 150
        y = 500
        font = pygame.font.Font("consola.ttf", 24)

        recoverButton_rect = pygame.draw.rect(screen, colors['white'], (x, y, width, height), 2)
        value_text = font.render('Recover', True, colors['yellow'])
        text_width, text_height = value_text.get_size()
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2
        screen.blit(value_text, (text_x, text_y))

    def drawUseRemains(self, screen):
        width = 150
        height = 50
        x = 1150
        y = 500
        font = pygame.font.Font("consola.ttf", 24)

        useRemains_rect = pygame.draw.rect(screen, colors['white'], (x, y, width, height), 2)
        value_text = font.render('Use Remains', True, colors['yellow'])
        text_width, text_height = value_text.get_size()
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2
        screen.blit(value_text, (text_x, text_y))

    def renderGameEnd(self, screen, bg, bg_rect, winner):
        
        font = pygame.font.Font("consola.ttf", 48)
        bg.fill((64,64,64))
        bg.set_alpha(200)
        screen.blit(bg, bg_rect)
        text = font.render(f"{winner} \nRed score:{self.players[0].score}\tBlue score:{self.players[0].score}", True, colors["white"])
        text_rect = text.get_rect()
        text_rect.center = (1400 // 2, 800 // 2)
        screen.blit(text, text_rect)

    def render(self, screen):
        self.drawBoard(screen, self.board)
        self.drawServants(screen, 'Blue', self.players[1].servants)
        self.drawServants(screen, 'Red', self.players[0].servants)
        self.drawExhausted(screen, 'Red', self.players[0].exhaustedServants)
        self.drawExhausted(screen, 'Blue', self.players[1].exhaustedServants)
        self.drawCollection(screen, 'Blue', self.players[1].collection)
        self.drawCollection(screen, 'Red', self.players[0].collection)
        #self.drawRecoverButton()
        #self.drawUseRemains()
    '''
    def playGame(self, train, log, render=False):
        '''
        if render:
            # Initialize Pygame
            pygame.init()
            # Set the window size
            window_size = (1400, 800)
            # Create the window
            screen = pygame.display.set_mode(window_size)
            pygame.display.set_caption('Crypt')
            bg = pygame.image.load('images/Background.png')
            bg_rect = bg.get_rect(topleft=(0,0))
            screen.blit(bg, bg_rect)
            '''
        game_over = False
        self.players[0].score = 0
        self.players[1].score = 0

        while not game_over:
            self.revealPhase()
            self.claimPhase(train, log)
            self.collectPhase()
            game_over = self.passTorchPhase(game_over)
        '''
        if render:
            if self.players[0].score > self.players[1].score:
                winner = 'Red wins'
            elif self.players[0].score < self.players[1].score:
                winner = 'Blue wins'
            else:
                winner = 'Tied Game'
            self.renderGameEnd(screen, bg, bg_rect, winner)
            pygame.display.flip()
            sleep(30)
            pygame.quit()
        '''