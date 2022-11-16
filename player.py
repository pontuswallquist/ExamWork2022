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

    def nr_servants(self):
        return len(self.servants)
    
    def hasTorch(self):
        return self.torch

    def recoverServants(self):
        self.servants = [Servant(self.color), Servant(self.color), Servant(self.color)]

    def recoverSingleServant(self):
        if len(self.servants) == 3:
            return
        self.servants.append(Servant(self.color))
    
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
    
    def hasRemains(self):
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