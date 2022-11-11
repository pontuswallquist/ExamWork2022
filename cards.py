import random
from player import Player

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
        self.coinvalue = value
        self.face_up = False

    def turnCard(self):
        self.face_up = not self.face_up

    def __repr__(self):
        if self.face_up:
            return str(cardtypes[self.type] + ' : ' + str(self.coinvalue))
        else:
            return str(cardtypes[self.type])


class CollectorCard:

    """A collector card."""
    def __init__(self, type, requirement):
        self.type = type
        self.requirement = requirement

    
    def __repr__(self):
        return str(self.requirement) +' : ' + cardtypes[self.type]


class RemainsCollector(CollectorCard):
    
    def __init__(self):
        super().__init__(1, 2)

    def useCard(self, player):
        count = 0
        for card in player.collection:
            if card.type == 1 and not card.face_up:
                count += 1
                card.turnCard()
            if count == 2:
                break             
        player.recoverSingleServant()

class IdolCollector(CollectorCard):
        
    def __init__(self):
        super().__init__(2, 1)
    
    def useCard(self, player):
        for card in player.collection:
            if card.type == 2 and not card.face_up:
                card.turnCard()
                return random.randint(1, 6)

class JewelryCollector(CollectorCard):

    def __init__(self):
        super().__init__(3, 2)

    def useCard(self, player):
        count = 0
        max_value = 0
        max_index = 0
        for index, card in enumerate(player.collection):
            if card.type == 3 and not card.face_up:
                count += 1
                if card.coinvalue > max_value:
                    max_value = card.coinvalue
                    max_index = index
        if count >= self.requirement:
            player.collection[max_index].coinvalue *= 2

class ManuscriptCollector(CollectorCard):
    
        def __init__(self):
            super().__init__(4, 2)
    
        def useCard(self, player):
            count = 0
            indexes = []
            for index, card in enumerate(player.collection):
                if card.type == 4:
                    count += 1
                    indexes.append(index)
            if count >= self.requirement:
                for manuscriptcard in indexes:
                    player.collection[manuscriptcard].coinvalue = 4

class PotteryCollector(CollectorCard):
        
    def __init__(self):
        super().__init__(5, 2)
        
    def useCard(self, player):
        count = 0
        for card in player.collection:
            if card.type == 5:
                count += 1
        if count == 2:
            player.score += 2
        elif count == 3:
            player.score += 4
        elif count >= 4:
            player.score += 8

class TapestryCollector(CollectorCard):

    def __init__(self):
        super().__init__(6, 1)

    def useCard(self, player1, player2):
        p1_score = 0
        p2_score = 0
        for card in player1.collection:
            if card.type == 6:
                p1_score += card.coinvalue
        for card in player2.collection:
            if card.type == 6:
                p2_score += card.coinvalue
        if p1_score > p2_score:
            player1.score += 5
        elif p2_score > p1_score:
            player2.score += 5
