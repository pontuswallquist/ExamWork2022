import random
from actionspace import Actions, ResultOfAction, ReducePossibleActions
import numpy as np
from rich.console import Console
from log_actions import log_action
import copy
console = Console()


def revealPhase(state):
    state.turnsLeft -= 1
    state.updateNewBoard(1)
    state.updateNewBoard(2)
    state.updateNewBoard(3)
    return state

def claimPhase(state, agent, train, log):

    #lostAServant = False
    # Penalty for lost servant last turn
    #if state.players[0].nr_servants_available() < 3:
    #    penalty = 10 * (state.players[0].nr_servants_available() - 3)
    #    lostAServant = True
    
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

            action, action_id = agent.step(state.get_input_state(), list_of_actions, actionspace, train)            

            if train is True or log is True:
                curr__input_state = copy.deepcopy(state.get_input_state())
                
            state, reward = ResultOfAction(state, 0, action)
            
            p0_played = True
            
            if log is True:
                console.print(curr__input_state, action, reward, state.get_input_state(), sep='\n', end='\n\n', justify='center', soft_wrap=True)
                #log_action(curr__input_state, action, 0)

            # call Remember with the state before action, action, reward, state after action, done
            if train is True:
                #reward += penalty
                done, reward = checkIfDone(state, action, reward, turn, p0_played)
                agent.remember(curr__input_state, action_id, reward, state.get_input_state(), done)
                agent.replay()
                
                if done:
                    if train is True:
                        agent.target_train()
                    turn += 1
                    continue

            if turn == 2 and state.players[0].hasTorch() and p0_played and p1_played:
                #if train is True:
                #    agent.target_train()
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
                curr__input_state = copy.deepcopy(state.get_input_state())
            state, _ = ResultOfAction(state, 1, action)
            p1_played = True

            if log is True:
                #log_action(curr__input_state, action, 1)
                pass

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
    state.players[0].score, state.players[1].score  = state.get_total_score()


    if state.turnsLeft == 0 and not hasAvailableActions(state, turn, hasPlayed) or state.turnsLeft == 0 and action == 'Recover':
        done = True
        reward = 10 * (state.players[0].score - state.players[1].score)
    else:
        done = False
    
    return done, reward

def hasAvailableActions(state, turn, hasPlayed):
    action_list, _ = Actions(state, 0, turn, hasPlayed)
    if len(action_list) == 0:
        return False
    else:
        return True
        

def playGame(state, agent, train, log):
    game_over = False
    while not game_over:
        state = revealPhase(state)
        state = claimPhase(state, agent, train, log)
        state = collectPhase(state)
        state, game_over = passTorchPhase(state, game_over)
    return state
