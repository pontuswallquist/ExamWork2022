

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

    servants_available = state.players[playerNr].nr_servants_available()

    if (playerNr == 0 and turn == 0 and not hasPlayed) or (playerNr == 1 and turn == 1 and not hasPlayed) or (playerNr == 0 and turn == 2 and not state.players[0].hasTorch() and not hasPlayed):
        if state.players[playerNr].hasExhaustedServants():
            actionspace[0][0] = 1
            actions.append('Recover')
        
    # Servant needs to be exhausted to be used by remains card or recover
    if state.players[playerNr].hasExhaustedServants():
        if state.players[playerNr].hasRemainsCards():
                actionspace[0][1] = 1
                actions.append('useRemains')

    if servants_available == 0:
        return actions, actionspace
    
    for place in state.board.keys():
        if len(state.board[place]['servants']) == 0:
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
    reward = 0
    if action == 'Recover':
        if state.players[playerNr].nr_servants_available() == 0:
            reward = 2
        elif state.players[playerNr].nr_servants_available() == 1:
            reward = 1
        elif state.players[playerNr].nr_servants_available() == 2:
            reward = 0
        state.players[playerNr].recoverAllExhaustedServants()

    elif action == 'useRemains':
        state.collectors[1].useCard(state.players[playerNr])
        reward = 5
    else:
        bid = action.split('-')

        place = int(bid[0])
        servant = int(bid[1])
        value = int(bid[2])

        
        bumped_off = state.addServant2Card(playerNr, place, servant, value)
        

        card = state.board[place]['card']

        #reward = state.board[place]['card'].coinvalue
        #reward += state.collectors[card.type].get_reward(state.players[playerNr])
       

        #subtract potential score for the player who was bumped off card
        otherPlayerNr = 1 if playerNr == 0 else 0
        if bumped_off:
            if card.type == 6:
                state.players[otherPlayerNr].score -= state.collectors[card.type].potentialValue(card, state.players[otherPlayerNr], state.players[playerNr])
            else:
                state.players[otherPlayerNr].score -= state.collectors[card.type].potentialValue(card, state.players[playerNr])

        #Add potential score for the player who owns the card
        if card.type == 6:
            reward = state.collectors[card.type].potentialValue(card, state.players[playerNr], state.players[otherPlayerNr])
        else:
            reward = state.collectors[card.type].potentialValue(card, state.players[playerNr])
        
        state.players[playerNr].score += reward

        #Times the probability of rolling equal or above the value of the servant
        if value == 1:
            reward *= 0.9
        else:
            reward *= ((7 - value) / 6)
        
    return state, reward

def ReducePossibleActions(actionspace, actions):
    actionspace1d = makeActionSpace1D(actionspace)
    for i in range(len(actionspace1d)):
        actions[i] = actions[i] * actionspace1d[i]
    return actions
