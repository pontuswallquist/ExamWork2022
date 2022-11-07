import random

board = {
    1: ['Red-3', 'Red-3'],
    2: [ ],
    3: ['Red-5']
}


def anyServants(color):
    for place in board:
        for servant in board[place]:
            if color in servant:
                return True
    return False


servants_to_roll = ['Red-3', 'Red-3', 'Blue-4', 'Red-5']


for servant in servants_to_roll:
    effort_value = servant.split('-')[1]
    color = servant.split('-')[0]
    if 'Red' in color:
        if state.players[0].hasIdol():
            state.rollWithAction(0)
        else:
            state.rollWithoutAction(0)

    elif 'Blue' in color:
        if state.players[1].hasIdol():
            state.rollWithAction(1)
        else:
            state.rollWithoutAction(1)
    print(servant)

            
print(servants_to_roll)
