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
        
    def recoverServants(self):
        self.servants = [Servant(self.color), Servant(self.color), Servant(self.color)]

    def recoverSingleServant(self):
        self.servants.append(Servant(self.color))
    
    def addTreasure(self, treasure):
        self.collection.append(treasure)




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

        

    
    

    



