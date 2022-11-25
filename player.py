import copy
from cards import *
import random


class Player:

    def __init__(self, color, torch = False):
        self.color = color
        self.torch = torch
        self.collection = []
        self.score = 0
        self.servants = { 1: Servant(color), 2: Servant(color), 3: Servant(color) }

    def useServant(self, value):
        for servant in self.servants.values():
            if servant.isExhausted or servant.onCard:
                continue
            else:
                servant.onCard = True
                servant.setValue(value)
                return servant

    def hasExhaustedServants(self):
        for servant in self.servants.values():
            if servant.isExhausted and not servant.onCard:
                return True
        return False


    def nr_servants_available(self):
        count = 0
        for servant in self.servants.values():
            if servant.isExhausted or servant.onCard:
                continue
            else:
                count += 1
        return count
    
    def hasTorch(self):
        return self.torch

    def ifAllServantsPushedOut(self):
        for servant in self.servants.values():
            if servant.onCard and not servant.isExhausted:
                return False
        return True

    def recoverAllExhaustedServants(self):
        for servant in self.servants.values():
            servant.isExhausted = False
            servant.onCard = False

    def bump_off_servant(self):
        for servant in self.servants.values():
            if servant.onCard and not servant.isExhausted:
                servant.onCard = False
                return
  
    def recoverExhaustedServant(self):
        for servant in self.servants.values():
            if servant.isExhausted and not servant.onCard:
                servant.isExhausted = False
                servant.onCard = False
                return

    def recoverServantFromCard(self):
        for servant in self.servants.values():
            if servant.onCard and not servant.isExhausted:
                servant.onCard = False
                servant.isExhausted = False
                return

    def exhaustAServant(self):
        for servant in self.servants.values():
            if not servant.isExhausted and servant.onCard:
                servant.isExhausted = True
                servant.onCard = False
                return
    
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

class Servant:

    def __init__(self, color):
        self.color = color
        self.value = 0
        self.effort_value = 0
        self.isExhausted = False
        self.onCard = False

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