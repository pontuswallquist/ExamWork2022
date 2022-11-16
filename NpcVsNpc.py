import random
from actionspace import Actions, ResultOfAction, ReducePossibleActions
import numpy as np
from rich.console import Console
console = Console()


map_actions_to_id = {
    'Recover': 0,
    'useRemains': 1,
    '1-1-1': 2, '1-1-2': 3, '1-1-3': 4, '1-1-4': 5, '1-1-5': 6, '1-1-6': 7,
    '1-2-1': 8, '1-2-2': 9, '1-2-3': 10, '1-2-4': 11, '1-2-5': 12, '1-2-6': 13,
    '1-3-1': 14, '1-3-2': 15, '1-3-3': 16, '1-3-4': 17, '1-3-5': 18, '1-3-6': 19,
    '2-1-1': 20, '2-1-2': 21, '2-1-3': 22, '2-1-4': 23, '2-1-5': 24, '2-1-6': 25,
    '2-2-1': 26, '2-2-2': 27, '2-2-3': 28, '2-2-4': 29, '2-2-5': 30, '2-2-6': 31,
    '2-3-1': 32, '2-3-2': 33, '2-3-3': 34, '2-3-4': 35, '2-3-5': 36, '2-3-6': 37,
    '3-1-1': 38, '3-1-2': 39, '3-1-3': 40, '3-1-4': 41, '3-1-5': 42, '3-1-6': 43,
    '3-2-1': 44, '3-2-2': 45, '3-2-3': 46, '3-2-4': 47, '3-2-5': 48, '3-2-6': 49,
    '3-3-1': 50, '3-3-2': 51, '3-3-3': 52, '3-3-4': 53, '3-3-5': 54, '3-3-6': 55
}

map_id_to_actions = {v: k for k, v in map_actions_to_id.items()}

def revealPhase(state):
    state.turnsLeft -= 1
    state.updateNewBoard(1)
    state.updateNewBoard(2)
    state.updateNewBoard(3)
    return state

def claimPhase(state, agent, train, train_target):
    
    if state.players[0].hasTorch():
        turn = 0
    else:
        turn = 1

    p0_played = False
    p1_played = False
    
    phase_over = False
    while not phase_over:

        if turn == 3 and state.players[0].hasTorch():
            break
        elif turn == 4 and state.players[1].hasTorch():
            break

        #Player Turn
        if turn % 2 == 0:
            list_of_actions, actionspace = Actions(state, 0, turn, p0_played) 
            if len(list_of_actions) == 0:
                turn += 1
                continue

            action_list = agent.step(state.get_input_state(0), list_of_actions, train)

            # if we got back a list, then take random action otherwise take the models action
            if isinstance(action_list, list):
                action = random.choice(action_list)
                action_id = map_actions_to_id[action]
            else:
                legal_outputs = ReducePossibleActions(actionspace, action_list)
                action_id = np.argmax(legal_outputs)
                action = map_id_to_actions[action_id]

            curr_state = state
            next_state, reward = ResultOfAction(curr_state, 0, action)
            # call Rembember with the state before action, action, reward, state after action
            if train is True:
                agent.remember(curr_state.get_input_state(0), action_id, reward, next_state.get_input_state(0))
                agent.replay()
                if train_target is True:
                    print('-----updating target network-----')
                    agent.target_train()
                    train_target = False

            state = next_state
            
            if action == 'Recover':
                p0_played = True
                turn += 1
                continue
     
            p0_played = True
            if turn == 2 and state.players[0].hasTorch() and p0_played and p1_played:
                phase_over = True
            
            if not state.players[0].servants:
                turn += 1
                continue
        
        #Opponent Turn
        elif turn % 2 == 1:   
            list_of_actions, _ = Actions(state, 1, turn, p1_played)
            if len(list_of_actions) == 0:
                turn += 1
                continue

            # Random action AI
            action = random.choice(list_of_actions)
            state, _ = ResultOfAction(state, 1, action)
            if action == 'Recover':
                p1_played = True
                turn += 1                
                continue

            p1_played = True
            if turn == 3 and state.players[1].hasTorch() and p0_played and p1_played:
                phase_over = True
            
            if not state.players[1].servants:
                turn += 1
                continue
    return state


def collectPhase(state):

    if not state.anyServants('Red'):
        state.players[0].recoverServants()
    if not state.anyServants('Blue'):
        state.players[1].recoverServants()
    

    state.collectCards()
    
    servants_to_roll = state.mergeServants()
    for servant in servants_to_roll:
        if servant.color == 'Red':
            if state.players[0].hasIdol():
                state.rollWithAction(0, servant)
            else:
                state.rollWithoutAction(0, servant)
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

def playGame(state, agent, train, train_target):
    game_over = False
    while not game_over:
        state = revealPhase(state)
        state = claimPhase(state, agent, train, train_target)
        state = collectPhase(state)
        state, game_over = passTorchPhase(state, game_over)
        train_target = False
    return state
