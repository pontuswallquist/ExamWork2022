from cards import *
import random
from collections import deque
import re

class PlayerInterface:

    def __init__(self, color, torch = False):
        self.color = color
        self.torch = torch
        self.collection = []
        self.score = 0
        self.servants = deque([Servant(color), Servant(color), Servant(color)], maxlen=3)
        self.exhaustedServants = deque([], maxlen=3)

        self.map_actions_to_id = {
            'Recover': 0,
            'useRemains': 1,
            '1-1-1': 2, '1-1-2': 3, '1-1-3': 4, '1-1-4': 5, '1-1-5': 6, '1-1-6': 7,
            '1-2-1': 8, '1-2-2': 9, '1-2-3': 10, '1-2-4': 11, '1-2-5': 12, '1-2-6': 13,
            '1-3-1': 14, '1-3-2': 15, '1-3-3': 16, '1-3-4': 17, '1-3-5': 18, '1-3-6': 19,
            '2-1-1': 20, '2-1-2': 21, '2-1-3': 22, '2-1-4': 23, '2-1-5': 24, '2-1-6': 25,
            '2-2-1': 26, '2-2-2': 27, '2-2-3': 28, '2-2-4': 29, '2-2-5': 30, '2-2-6': 31,
            '2-3-1': 32, '2-3-2': 33, '2-3-3': 34, '2-3-4': 35, '2-3-5': 36, '2-3-6': 37,
            '3-1-1': 38, '3-1-2': 39, '3-1-3': 40, '3-1-4': 41, '3-1-5': 42, '3-1-6': 43,
            '3-2-1': 44, '3-2-2': 45, '3-2-3': 46, '3-2-4': 47, '3-2-5': 48, '3-2-6': 49,
            '3-3-1': 50, '3-3-2': 51, '3-3-3': 52, '3-3-4': 53, '3-3-5': 54, '3-3-6': 55
        }

        self.map_id_to_actions = {v: k for k, v in self.map_actions_to_id.items()}

    def reset(self):
        self.collection = []
        self.score = 0
        self.servants = deque([Servant(self.color), Servant(self.color), Servant(self.color)], maxlen=3)
        self.exhaustedServants = deque([], maxlen=3)

    def useServant(self, value):
        servant = self.servants.pop()
        servant.setValue(value)
        return servant

    def hasExhaustedServants(self):
        if self.exhaustedServants:
            return True
        return False

    def nr_servants_available(self):
        return len(self.servants)
    
    def hasTorch(self):
        return self.torch

    def recoverAllExhaustedServants(self):
        for i in range(len(self.exhaustedServants)):
            servant = self.exhaustedServants.pop()
            self.servants.append(servant)
            
    def bump_off_servant(self, servant):
        self.servants.append(servant)
  
    def recoverExhaustedServant(self):
        servant = self.exhaustedServants.pop()
        self.servants.append(servant)

    def recoverServantFromCard(self, servant):
        self.servants.append(servant)

    def exhaustAServant(self, servant):
        self.exhaustedServants.append(servant)
    
    def addTreasure(self, treasure):
        self.collection.append(treasure)

    def turnAllCards(self):
        for card in self.collection:
            if not card.face_up:
                card.turnCard()
    
    def hasIdol(self):
        count = sum(1 for x in self.collection if x.type == 2 and not x.face_up)
        if count >= 1:
            return True
        else:
            return False
    
    def hasRemainsCards(self):
        count = sum(1 for x in self.collection if x.type == 1 and not x.face_up)
        if count >= 2:
            return True
        else:
            return False

    def nr_remains(self):
        count = sum(1 for x in self.collection if x.type == 1)
        return count

    def nr_idols(self):
        count = sum(1 for x in self.collection if x.type == 2)
        return count

    def nr_jewelry(self):
        count = sum(1 for x in self.collection if x.type == 3)
        return count
    
    def nr_manuscripts(self):
        count = sum(1 for x in self.collection if x.type == 4)
        return count
    
    def nr_pottery(self):
        count = sum(1 for x in self.collection if x.type == 5)
        return count
    
    def nr_tapestries(self):
        count = sum(1 for x in self.collection if x.type == 6)
        return count

class HumanPlayer(PlayerInterface):
    
    def __init__(self, color, torch=False):
        super().__init__(color, torch)
    
    def step(self, input_state, list_of_possible_actions, actionspace, train):

        options = []
        if 'Recover' in list_of_possible_actions:
            options.append('Recover')
        if 'useRemains' in list_of_possible_actions:
            options.append('useRemains')
        if self.servants:
            options.append('Claim')

        print('Choose an action:')
        for i, option in enumerate(options):
            print(i, ':', option)
        action = int(input())
        action = options[action]
        if action == 'Claim':
            if len(list_of_possible_actions) < 10:
                print(list_of_possible_actions)
            print("Please enter bid in the form of place-servants-value:")
            validInput = False
            while not validInput:
                action = input()
                pattern = re.compile(r'(\d)-(\d)-(\d)')
                match = pattern.fullmatch(action)
                if match:
                    if action in list_of_possible_actions:
                        validInput = True
                    else:
                        print("Invalid input, please try again")
                else:
                    print("Invalid input, please try again")
        
        action_id = self.map_actions_to_id[action]
        return action, action_id
      
class RandomPlayer(PlayerInterface):

    def __init__(self, color, torch=False):
        super().__init__(color, torch)
        

    def step(self, input_state, list_of_possible_actions, actionspace, train):
        action = random.choice(list_of_possible_actions)
        action_id = self.map_actions_to_id[action]
        return action, action_id

class Servant:

    def __init__(self, color):
        self.color = color
        self.value = 1
        self.effort_value = 0

    def __repr__(self):
        return str(self.color + '-' + str(self.value))

    def roll(self):
        return random.randint(1, 6)

    def setEffort(self, value):
        self.effort_value = value

    def getEffort(self):
        return self.effort_value

    def setValue(self, value):
        self.value = value