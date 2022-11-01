import random

class TreasureCard:
    
    """A treasure card."""
    def __init__(self, name, type, value, face_up):
        self.name = name
        self.face_up = face_up
        self.type = type
        self.value = value



class CollectorCard:

    """A collector card."""
    def __init__(self,type, requirement, reward):
        self.type = type
        self.reward = reward
        self.requirement = requirement


class Servant:

    def roll(self):
        return random.randint(1,6)

    def seteffortvalue(self, effort_value):
        self.effort_value = effort_value
    

class LeaderCard:

    def __init__(self):
        self.type = "Torch"

class LightsOut:

    def __init__(self):
        self.type = "Lights Out"
        