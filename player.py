from cards import *
import random


class Player:

    def __init__(self, color, torch = False):
        self.color = color
        self.torch = torch
        self.collection = []
        self.score = 0
        self.servants = [Servant(self.color), Servant(self.color), Servant(self.color)]

    def useServant(self, value):
        servant = self.servants.pop()
        servant.setValue(value)
        return servant

    def hasLessThan3Servants(self):
        return len(self.servants) < 3
    
    def hasTorch(self):
        return self.torch

    def recoverServants(self):
        self.servants = [Servant(self.color), Servant(self.color), Servant(self.color)]

    def recoverSingleServant(self):
        self.servants.append(Servant(self.color))
    
    def addTreasure(self, treasure):
        self.collection.append(treasure)

    def turnAllCards(self):
        for card in self.collection:
            if not card.face_up:
                card.turnCard()
    
    def hasIdol(self):
        for card in self.collection:
            if card.type == 2 and not card.face_up:
                return True
        return False
    
    def hasRemains(self):
        count = 0
        for card in self.collection:
            if card.type == 1 and not card.face_up:
                count += 1
            if count == 2:
                return True
        return False

class Servant:

    def __init__(self, color):
        self.color = color
        self.value = 0
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