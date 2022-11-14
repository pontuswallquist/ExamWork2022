

gamestate = crypt.Crypt()
gamestate.updateNewBoard(1)
gamestate.updateNewBoard(2)
gamestate.updateNewBoard(3)

gamestate.addServant2Card(0, 2, 2, 2)
gamestate.addServant2Card(0, 3, 1, 2)

actions, actionspace = Actions(gamestate, 1, 1, False)
actionspace1d = makeActionSpace1D(actionspace)



def ReducePossibleActions(actionspace1d, actions):
    for i in range(len(actionspace1d)):
        actions[i] = actions[i] * actionspace1d[i]
    return actions


# To use the model and get the action

state_tensor = tf.convert_to_tensor(np.array([1, 4, 2])) # Input state
state_tensor = tf.expand_dims(state_tensor, 0)
action_probs = model(state_tensor, training=False)




# Reduce the actions to the possible actions
legal_actions = ReducePossibleActions(actionspace1d, action_probs[0].numpy())
print(legal_actions)

#Pick the action with highest value
action = tf.argmax(legal_actions).numpy()
print(action)