import crypt
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Input, Softmax
from keras.optimizers import Adam

total_actions_possible = 56
total_states_possible = 3


gamma = 0.95
epsilon = 1.0
epsilon_min = 0.01
epsilon_decay = 0.995
learning_rate = 0.01


def basicModel(nr_states, nr_actions):
    inputs = Input(shape=(nr_states,))
    layer1 = Dense(24, activation='relu')(inputs)
    action = Dense(nr_actions, activation='softmax')(layer1)
    return keras.Model(inputs=inputs, outputs=action)

model = basicModel(total_states_possible, total_actions_possible)
model.summary()

optimizer = Adam(learning_rate=learning_rate)

model.compile(optimizer=optimizer, loss='mse')

actionspace = [
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
    ]


# To use the model and get the action
state_tensor = tf.convert_to_tensor(np.array([1, 4, 2])) # Input state
state_tensor = tf.expand_dims(state_tensor, 0)
action_probs = model(state_tensor, training=False)
print(action_probs)
action = tf.argmax(action_probs[0]).numpy()
print(action)