import numpy as np
import random
from keras.layers import Input, Dense
from keras.models import Model, load_model

from keras.optimizers import Adam, SGD
from collections import deque
from actionspace import *
import tensorflow as tf

class ReplayMemory:
    def __init__(self, max_size):
        self.buffer = [None] * max_size
        self.max_size = max_size
        self.index = 0
        self.size = 0

    def append(self, obj):
        self.buffer[self.index] = obj
        self.size = min(self.size + 1, self.max_size)
        self.index = (self.index + 1) % self.max_size

    def sample(self, batch_size):
        indices = random.sample(range(self.size), batch_size)
        return [self.buffer[index] for index in indices]


class DQNAgent:
    def __init__(self, learning_rate=0.001, epsilon=1.0, epsilon_decay=0.995 , gamma=0.95):
        self.memory = ReplayMemory(10000)
        self.gamma = gamma    # discount rate
        self.epsilon = epsilon # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.training_history = None
        self.nr_actions = 56
        self.nr_states = 25


        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        input_layer = Input(shape=(self.nr_states,))
        hidden_layer = Dense(40, activation='relu')(input_layer)
        output_layer = Dense(self.nr_actions, activation='linear')(hidden_layer)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.learning_rate), metrics=['accuracy'])
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
        output = self.model(inputs)[0].numpy()
        return output

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return
        samples = self.memory.sample(batch_size)
        for sample in samples:
            input_state, action, reward, next_state, done = sample
            inputs = tf.expand_dims(input_state, 0) # make tensorflow tensor
            target = self.target_model(inputs, training=True)[0].numpy()
            
            if done:
                target[action] = reward
            else:
                next_inputs = tf.expand_dims(next_state, 0)
                Q_future = max(self.target_model(next_inputs, training=True)[0].numpy())
                target[action] = reward + Q_future * self.gamma
                target = tf.expand_dims(target, 0)
                self.training_history = self.model.fit(inputs, target, epochs=1, verbose=0)
                
    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i]
        self.target_model.set_weights(target_weights)

    def save_model(self, file_name):
        self.model.save(file_name)

    def load_model(self, file_name):
        self.model = load_model(file_name)

    