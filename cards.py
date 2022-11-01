import random

cardtypes = {
    1: 'Remains',
    2: 'Idol',
    3: 'Jewelry',
    4: 'Manuscript',
    5: 'Pottery',
    6: 'Tapestry'
}

class TreasureCard:
    
    """A treasure card."""
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.face_up = False

    def turnCard(self):
        self.face_up = not self.face_up

    def __repr__(self):
        if self.face_up:
            return cardtypes[self.type] + ' : ' + str(self.value)
        else:
            return cardtypes[self.type]


class CollectorCard:

    """A collector card."""
    def __init__(self, type, requirement, reward):
        self.type = type
        self.reward = reward
        self.requirement = requirement

class LeaderCard:

    def __init__(self):
        self.type = "Leader"

class LightsOut:

    def __init__(self):
        self.type = "Lights Out"