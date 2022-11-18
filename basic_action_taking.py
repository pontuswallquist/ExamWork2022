import crypt as crypt
from actionspace import Actions, makeActionSpace1D, ActiontoIndex, ReducePossibleActions, ResultOfAction
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Input, Softmax
from keras.optimizers import Adam

total_actions_possible = 56
total_states_possible = 25


gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
learning_rate = 0.01


def createModel(nr_states, nr_actions):
    inputs = Input(shape=(nr_states,))
    layer1 = Dense(40, activation='relu')(inputs)
    outputs = Dense(nr_actions, activation='softmax')(layer1)
    model = keras.Model(inputs=inputs, outputs=outputs, name='DQN')
    optimizer = Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

model = createModel(total_states_possible, total_actions_possible)
model.summary()

gamestate = crypt.Crypt()
gamestate.updateNewBoard(1)
gamestate.updateNewBoard(2)
gamestate.updateNewBoard(3)

gamestate.addServant2Card(0, 2, 2, 2)
gamestate.addServant2Card(0, 3, 1, 2)

actions, actionspace = Actions(gamestate, 1, 1, False)
#actionspace1d = makeActionSpace1D(actionspace)

# To get outputs from the model
inputs = tf.expand_dims(gamestate.get_input_state(), 0)
output = model(inputs)[0].numpy()

target = tf.expand_dims(output, 0)

#print(output)





'''
legal_outputs = ReducePossibleActions(actionspace, output)
action = np.argmax(legal_outputs)

print(legal_outputs)
print(action)
'''
