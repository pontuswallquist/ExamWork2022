import random
from player import *

cardtypes = {
    1: 'Remains',
    2: 'Idol',
    3: 'Jewelry',
    4: 'Manuscript',
    5: 'Pottery',
    6: 'Tapestry'
}

shortcardtypes = {
    1: 'R',
    2: 'I',
    3: 'J',
    4: 'M',
    5: 'P',
    6: 'T'
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
        player.recoverExhaustedServant()
    
    def get_score(self, player):
        score = sum(x.coinvalue for x in player.collection if x.type == 1)
        return score

    def potentialValue(self, card, player1=None, player2=None):
        return card.coinvalue

    def get_reward(self, player):
        nr_eligible_cards = sum(1 for x in player.collection if x.type == 1 and not x.face_up)
        if nr_eligible_cards >= 1:
            return 2
        else:
            return 0

class IdolCollector(CollectorCard):
        
    def __init__(self):
        super().__init__(2, 1)
    
    def useCard(self, player):
        for card in player.collection:
            if card.type == 2 and not card.face_up:
                card.turnCard()
                return random.randint(1, 6)
        
    def get_score(self, player):
        score = sum(x.coinvalue for x in player.collection if x.type == 2)
        return score

    def potentialValue(self, card, player1=None, player2=None):
        return card.coinvalue
        
    def get_reward(self, player):
        return 1

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

    def get_score(self, player):
        score = 0
        jewelry_cards = [x for x in player.collection if x.type == 3]
        if len(jewelry_cards) >= 2:
            for card in jewelry_cards:
                score += card.coinvalue
            score += max(card.coinvalue for card in jewelry_cards)
            return score
        else:
            for card in jewelry_cards:
                score += card.coinvalue
            return score

    def get_reward(self, player):
        nr_eligible_cards = sum(1 for x in player.collection if x.type == 3)
        if nr_eligible_cards == 1:
            return 2
        else:
            return 0

    def potentialValue(self, card, player1=None, player2=None):
        val = card.coinvalue
        eligible_cards = [x for x in player1.collection if x.type == 3]
        if len(eligible_cards) == 1:
            max_value = max(x.coinvalue for x in eligible_cards)
            if val >= max_value:
                val *= 2
            else:
                val = max_value*2
        return val

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

        def get_score(self, player):
            score = 0
            manuscript_cards = [x for x in player.collection if x.type == 4]
            if len(manuscript_cards) >= 2:
                for card in manuscript_cards:
                    score += 4
                return score
            else:
                for card in manuscript_cards:
                    score += card.coinvalue
                return score

        def potentialValue(self, card, player1=None, player2=None):
            val = card.coinvalue
            eligible_cards = [x for x in player1.collection if x.type == 4]
            if len(eligible_cards) >= 1:
                val = 4
            return val

        def get_reward(self, player):
            nr_eligible_cards = sum(1 for x in player.collection if x.type == 4)
            if nr_eligible_cards >= 1:
                return 4
            else:
                return 0

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

    def get_score(self, player):
        score = 0
        pottery_cards = [x for x in player.collection if x.type == 5]
        if len(pottery_cards) == 2:
            for card in pottery_cards:
                score += card.coinvalue
            score += 2
            return score
        elif len(pottery_cards) == 3:
            for card in pottery_cards:
                score += card.coinvalue
            score += 4
            return score
        elif len(pottery_cards) >= 4:
            for card in pottery_cards:
                score += card.coinvalue
            score += 8
            return score
        else:
            for card in pottery_cards:
                score += card.coinvalue
            return score

    def potentialValue(self, card, player1=None, player2=None):
        val = card.coinvalue
        eligible_cards = [x for x in player1.collection if x.type == 5]
        if len(eligible_cards) == 1:
            val += 2
        elif len(eligible_cards) == 2:
            val += 4
        elif len(eligible_cards) == 3:
            val += 8
        return val

    def get_reward(self, player):
        nr_eligible_cards = sum(1 for x in player.collection if x.type == 5)
        if nr_eligible_cards == 1:
            return 2
        elif nr_eligible_cards == 2:
            return 4
        elif nr_eligible_cards == 3:
            return 8
        else:
            return 0

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

    def get_score(self, player1, player2):
        player1_score = 0
        player2_score = 0
        tapestry_1 = [x for x in player1.collection if x.type == 6]
        tapestry_2 = [x for x in player2.collection if x.type == 6]
        for card in tapestry_1:
            player1_score += card.coinvalue
        for card in tapestry_2:
            player2_score += card.coinvalue
        if player1_score > player2_score:
            player1_score += 5
            return player1_score, player2_score
        elif player2_score > player1_score:
            player2_score += 5
            return player1_score, player2_score
        else:
            player1_score += 5
            player2_score += 5
            return player1_score, player2_score

    def potentialValue(self, card, player1=None, player2=None):
        p1_sum = sum(x.coinvalue for x in player1.collection if x.type == 6)
        p2_sum = sum(x.coinvalue for x in player2.collection if x.type == 6)
        if p1_sum + 1 >= p2_sum:
            return card.coinvalue + 5
        else:
            return card.coinvalue
    
    def get_reward(self, player):
        return 2