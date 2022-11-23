import random
from actionspace import Actions, ResultOfAction, ReducePossibleActions
import numpy as np
from rich.console import Console
from log_actions import log_action
import copy
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

def claimPhase(state, agent, train, train_target, log):
    
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

            # return a single action
            outputs = agent.step(state.get_input_state(), list_of_actions, train)

            # if outputs is a list, then take random action, otherwise its a numpy array
            if isinstance(outputs, list):
                action = random.choice(outputs)
                action_id = map_actions_to_id[action]
            else:
                legal_outputs = ReducePossibleActions(actionspace, outputs)
                action_id = np.argmax(legal_outputs)
                action = map_id_to_actions[action_id]

            if train is True or log is True:
                curr_state = copy.deepcopy(state)
            state, reward = ResultOfAction(state, 0, action)
            
            p0_played = True
            
            if log is True:
                console.print(curr_state.get_input_state(), action, reward, state.get_input_state(), sep='\n', end='\n\n')
                log_action(curr_state, action, 0)
                del curr_state

            # call Remember with the state before action, action, reward, state after action, done
            if train is True:
                done, reward = checkIfDone(state, action, reward, turn, p0_played)
                agent.remember(curr_state.get_input_state(), action_id, reward, state.get_input_state(), done)
                del curr_state
                agent.replay()
                if train_target is True:
                    agent.target_train()
                    train_target = False
                if done:
                    turn += 1
                    continue

            if turn == 2 and state.players[0].hasTorch() and p0_played and p1_played:
                phase_over = True

            if action == 'Recover':
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
            if log is True:
                curr_state = copy.deepcopy(state)
            state, _ = ResultOfAction(state, 1, action)
            p1_played = True

            if log is True:
                log_action(curr_state, action, 1)
                del curr_state


            if turn == 3 and state.players[1].hasTorch() and p0_played and p1_played:
                phase_over = True
            
            if action == 'Recover':
                turn += 1                
                continue

    return state


def collectPhase(state):

    if state.players[0].ifAllServantsPushedOut():
        state.players[0].recoverAllExhaustedServants()
    elif state.players[1].ifAllServantsPushedOut():
        state.players[1].recoverAllExhaustedServants()
    

    state.collectCards()
    state.players[0].score = 0
    state.players[1].score = 0
    state.players[0].score, state.players[1].score = state.get_total_score()
    
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
        # reset score and count score
        state.players[0].score = 0
        state.players[1].score = 0
        state.countBonus()
        state.calculateCollectionScore()
        state.countServants()
        game_over = True
    else:
        state.players[0].torch = not state.players[0].torch
        state.players[1].torch = not state.players[1].torch
        game_over = False
    return state, game_over

def checkIfDone(state, action, reward, turn, hasPlayed):

    state.players[0].score = 0
    state.players[1].score = 0
    model_score, opponent_score = state.get_total_score()
    state.players[0].score = model_score
    state.players[1].score = opponent_score

    diff = model_score - opponent_score

    if state.turnsLeft == 0 and not hasAvailableActions(state, turn, hasPlayed) or state.turnsLeft == 0 and action == 'Recover':
        done = True
        reward = 5 * diff
    else:
        done = False
        return done, reward

def hasAvailableActions(state, turn, hasPlayed):
    action_list, _ = Actions(state, 0, turn, hasPlayed)
    if len(action_list) == 0:
        return False
    else:
        return True
        

def playGame(state, agent, train, train_target, log):
    game_over = False
    while not game_over:
        state = revealPhase(state)
        state = claimPhase(state, agent, train, train_target, log)
        state = collectPhase(state)
        state, game_over = passTorchPhase(state, game_over)
        train_target = False
    return state
