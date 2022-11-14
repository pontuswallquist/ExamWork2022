import numpy as np
import random
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import Adam
from collections import deque

class DQNAgent:
    def __init__(self):
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999
        self.learning_rate = 0.005
        self.nr_actions = 56
        self.nr_states = 3

        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        input_layer = Input(shape=(self.nr_states,))
        hidden_layer = Dense(24, activation='relu')(input_layer)
        output_layer = Dense(self.nr_actions, activation='linear')(hidden_layer)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))



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

    