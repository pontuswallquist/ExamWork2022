import crypt
import random
from actionspace import Actions, ResultOfAction, getPlayerAction
from rich.console import Console
console = Console()

def revealPhase(state):
    state.turnsLeft -= 1
    console.print('[bold underline italic green]Reveal Phase', justify='center')
    console.print('Turns left: ', state.turnsLeft, justify='left')
    
    state.updateNewBoard(1)
    state.updateNewBoard(2)
    state.updateNewBoard(3)
    return state

def claimPhase(state):
    
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
            state.printBoard()
            state.printRoundInfo(0)
            list_of_actions, _ = Actions(state, 0, turn, p0_played) 
            if len(list_of_actions) == 0:
                console.print('[bold red]You have no possible actions', justify='left')
                turn += 1
                continue

            action = getPlayerAction(list_of_actions)
            state = ResultOfAction(state, 0, action)
            console.print('[red]You played: ', action, justify='left')
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
            state.printBoard()
            state.printRoundInfo(1)
            list_of_actions, actionspace = Actions(state, 1, turn, p1_played)
            if len(list_of_actions) == 0:
                console.print('[bold blue]You have no possible actions', justify='right')
                turn += 1
                continue
            #action = getAIAction(state, list_of_actions)
            # get random action
            action = random.choice(list_of_actions)
            state = ResultOfAction(state, 1, action)
            console.print('[blue]NPC played: ', action, justify='right')
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

    console.print('[bold underline italic green]Collect Phase', justify='center')
    state.printBoard()

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
        input('Press enter to pass the torch')
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

def main():
    state = crypt.Crypt()
    state = playGame(state)
    state.printScore()
    if state.players[0].score > state.players[1].score:
        console.print('[bold red]You won!', justify='center')
    elif state.players[0].score < state.players[1].score:
        console.print('[bold blue]NPC won!', justify='center')
    else:
        print('It is a tie with a score of ' + str(state.players[0].score))


main()