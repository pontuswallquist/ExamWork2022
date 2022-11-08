
def Actions(state, playerNr, turn, hasPlayed):
    actions = []
    servants_available = len(state.players[playerNr].servants)
    if (playerNr == 1 and turn == 1 and not hasPlayed) or (playerNr == 0 and turn == 0 and not hasPlayed) or (playerNr == 0 and turn == 2 and not state.players[0].hasTorch() and not hasPlayed):
        if servants_available < 3:
            actions.append('Recover')
            if state.players[playerNr].hasRemains():
                actions.append('UseRemains')
    if servants_available == 0:
        return actions
    
    for place in state.board.keys():
        if not state.board[place]['servants']:
            for servant in range(1, servants_available + 1):
                for value in range(1,7):
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
                        actions.append(str(place) + '-' + str(servant) + '-' + str(value))

    return actions

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

    




            
    
    

    
    
    
    