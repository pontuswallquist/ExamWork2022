

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
    actionspace = [
    [0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    actions = []
    servants_available = len(state.players[playerNr].servants)
    if (playerNr == 1 and turn == 1 and not hasPlayed) or (playerNr == 0 and turn == 0 and not hasPlayed) or (playerNr == 0 and turn == 2 and not state.players[0].hasTorch() and not hasPlayed):
        if servants_available < 3:
            actionspace[0][0] = 1
            actions.append('Recover')
            if state.players[playerNr].hasRemains():
                actionspace[0][1] = 1
                actions.append('useRemains')
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
        reward = 3
    elif action == 'useRemains':
        state.collectors[1].useCard(state.players[playerNr])
        reward = 5
    else:
        place, servant, value = action.split('-')
        place = int(place)
        servant = int(servant)
        value = int(value)
        state.addServant2Card(playerNr, place, servant, value)
        card_type = state.board[place]['card'].type

        reward = state.board[place]['card'].coinvalue
        reward += state.collectors[card_type].get_reward(state.players[playerNr])
        
    return state, reward

def ReducePossibleActions(actionspace, actions):
    actionspace1d = makeActionSpace1D(actionspace)
    for i in range(len(actionspace1d)):
        actions[i] = actions[i] * actionspace1d[i]
    return actions
