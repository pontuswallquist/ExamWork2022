from rich.console import Console
from rich.table import Table
console = Console()

actionspace = [
    [0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def ActiontoIndex(place, servant, value):
    servantIndex = servant - 1
    valueIndex = value - 1
    rowIndex = place
    columnIndex = servantIndex * 6 + valueIndex
    return rowIndex, columnIndex

def makeActionSpace1D(actionspace):
    actionspace1D = []
    actionspace1D.extend(actionspace[0])
    actionspace1D.extend(actionspace[1])
    actionspace1D.extend(actionspace[2])
    actionspace1D.extend(actionspace[3])
    return actionspace1D


def Actions(state, playerNr, turn, hasPlayed):
    actions = []
    servants_available = len(state.players[playerNr].servants)
    if (playerNr == 1 and turn == 1 and not hasPlayed) or (playerNr == 0 and turn == 0 and not hasPlayed) or (playerNr == 0 and turn == 2 and not state.players[0].hasTorch() and not hasPlayed):
        if servants_available < 3:
            actionspace[0][0] = 1
            actions.append('Recover')
            if state.players[playerNr].hasRemains():
                actionspace[0][1] = 1
                actions.append('UseRemains')
    if servants_available == 0:
        return actions, actionspace
    
    for place in state.board.keys():
        if not state.board[place]['servants']:
            for servant in range(1, servants_available + 1):
                for value in range(1,7):
                    # If action is valid, add it to the list of actions and add it to the action space
                    rowIndex, columnIndex = ActiontoIndex(place, servant, value)
                    actionspace[rowIndex][columnIndex] = 1
                    actions.append(str(place) + '-' + str(servant) + '-' + str(value))
        else:
            #If place is occupied, check if player already has a servant there
            if state.board[place]['servants'][0].color == state.players[playerNr].color:
                continue
            #If there are servants on the board, check if the player can outbid the current bid
            current_bid = 0
            for dice in state.board[place]['servants']:
                current_bid += dice.value
            for servant in range(1, servants_available + 1):
                for value in range(1,7):
                    if current_bid < value*servant:
                        rowIndex, columnIndex = ActiontoIndex(place, servant, value)
                        actionspace[rowIndex][columnIndex] = 1
                        actions.append(str(place) + '-' + str(servant) + '-' + str(value))

    return actions, actionspace

def ResultOfAction(state, playerNr, action):
    if action == 'Recover':
        state.players[playerNr].recoverServants()
    elif action == 'UseRemains':
        state.collectors[1].useCard(state.players[playerNr])
    else:
        place, servant, value = action.split('-')
        place = int(place)
        servant = int(servant)
        value = int(value)
        state.addServant2Card(playerNr, place, servant, value)
    
    return state

def printAvailableActions(list_of_actions):
    place1_actions = []
    place2_actions = []
    place3_actions = []
    other_actions = []
    for i, action in enumerate(list_of_actions):
        if action == 'Recover':
            other_actions.append((i,action))
        elif action == 'UseRemains':
            other_actions.append((i,action))
        else:
            place = action.split('-')[0]
            if place == '1':
                place1_actions.append((i, action))
            elif place == '2':
                place2_actions.append((i, action))
            elif place == '3':
                place3_actions.append((i, action))

    if len(place1_actions) == len(place2_actions) == len(place3_actions):
        for i in range(len(other_actions)):
            console.print(f'{other_actions[i][0]}: {other_actions[i][1]}')
        for i in range(len(place1_actions)):
            console.print(f'{place1_actions[i][0]}: {place1_actions[i][1]}', f'{place2_actions[i][0]}: {place2_actions[i][1]}', f'{place3_actions[i][0]}: {place3_actions[i][1]}')
    
    else:
        for i, action in enumerate(list_of_actions):
            console.print(i,':',str(action), end=' || ')
    console.print('')


def getPlayerAction(list_of_actions):

    console.print('\nPlace-NrOfServants-Value\n')
    printAvailableActions(list_of_actions)
    
    
    while True:
        try:
            action = int(input('Choose an action --> '))
            if action < 0 or action > len(list_of_actions) - 1:
                raise ValueError
            break
        except ValueError:
            print('Invalid input. Try again.')
    return list_of_actions[action]
    




            
    
    

    
    
    
    
