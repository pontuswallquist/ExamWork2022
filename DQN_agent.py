import numpy as np
import random
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import Adam
from collections import deque
from actionspace import *
from crypt import crypt
import tensorflow as tf

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

    def step(self, input_state, action_list, train):
        if train:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon_min, self.epsilon)

            if np.random.random() < self.epsilon:
                return action_list
        
        inputs = tf.expand_dims(input_state, 0)
        output = self.model.predict(inputs)[0]
        return output

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return
        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            input_state, action, reward, next_state, done = sample
            inputs = tf.expand_dims(input_state, 0)
            target = self.target_model.predict(inputs)
            if done:
                target[0][action] = reward
            

    def get_prediction(self, state, action_list, action_space, target=False):
        state_tensor = tf.convert_to_tensor(state)
        state_tensor = tf.expand_dims(state_tensor, 0)
        #get the valued actions from the model
        if target:
            action_probs = self.target_model(state_tensor, training=False)
        else:
            action_probs = self.model(state_tensor, training=False)

        action_probs = action_probs[0].numpy()
        #reduce the actions to the possible actions
        legal_actions = ReducePossibleActions(action_space, action_probs)
        #pick the action with highest value
        action_id = tf.argmax(legal_actions).numpy()
        action = action_list[action_id]
        return action



    