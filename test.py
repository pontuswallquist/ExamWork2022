import random
import crypt
from gameVSai import *



board = {
    1: [1, 2, 3],
    2: [4, 5, 6],
    3: [7, 8, 9]
}

state = crypt.Crypt()
state = revealPhase(state)
state.addServant2Card(1, 1, 1, 1)
state.addServant2Card(1, 2, 1, 1)


def anyServants(state, color):
        for place in state.board.keys():
            for servant in state.board[place]['servants']:
                if servant.color == color:
                    return True
        return False
