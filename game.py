import crypt
import random

def revealPhase(state):
    state.updateNewBoard(1)
    state.updateNewBoard(2)
    state.updateNewBoard(3)
    return state

def claimPhase(state):
    
    if state.players[0].hasTorch():
        turn = 0
    else:
        turn = 1
    
    phase_over = False
    while not phase_over:

        #Player Turn
        if turn % 2 == 0:
            list_of_actions = Actions(state, 1)
            if len(list_of_actions) == 0:
                turn += 1
                continue
            action = getPlayerAction(state, list_of_actions)
            state = ResultOfAction(state, action)
            if action == 'Recover':
                turn += 1
                continue
            if turn == 2 and state.players[0].hasTorch():
                phase_over = True

        #Opponent Turn
        elif turn % 2 == 1:
            list_of_actions = Actions(state, 2)
            if len(list_of_actions) == 0:
                turn += 1
                continue
            #action = getAIAction(state, list_of_actions)
            # get random action
            action = random.choice(list_of_actions)
            state = ResultOfAction(state, action)
            if action == 'Recover':
                turn += 1
                continue
            if turn == 3:
                phase_over = True
    
    return state


def collectPhase(state):
    state.collectCards()

    if not state.anyServants('Red'):
        state.players[0].recoverAllServants()
    if not state.anyServants('Blue'):
        state.players[1].recoverAllServants()
    
    servants_to_roll = state.mergeServants()
    for servant in servants_to_roll:
        if servant.color == 'Red':
            if state.players[0].hasIdol():
                state.rollWithAction(0, servant)
            else:
                state.rollWithoutAction(0)
        elif servant.color == 'Blue':
            if state.players[1].hasIdol():
                state.rollWithAction(1, servant)
            else:
                state.rollWithoutAction(1, servant)

    return state

def passTorchPhase(state, game_over):
    if not state.deck:
        state.countBonus()
        state.calculateCollectionScore()
        state.countServants()
        game_over = True
    else:
        state.players[0].torch = not state.players[0].torch
        state.players[1].torch = not state.players[1].torch
        game_over = False
    return state, game_over

def playGame(state):
    game_over = False
    while not game_over:
        state = revealPhase(state)
        state = claimPhase(state)
        state = collectPhase(state)
        state, game_over = passTorchPhase(state, game_over)
    return state