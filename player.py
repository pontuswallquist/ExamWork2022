from cards import *
import random

class Player:

    def __init__(self, id, torch = False):
        self.id = id
        self.torch = torch
        self.collection = []
        self.score = 0
        self.servants = [Servant(self.id), Servant(self.id), Servant(self.id)]
        
# Fixa id för servants och spelare    


class Servant:

    def __init__(self, belongs_to):
        self.belongs_to = belongs_to



        

    
    

    



