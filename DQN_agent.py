import numpy as np
import random
from keras.layers import Input, Dense
from keras.models import Model, load_model
from actionspace import ReducePossibleActions

from keras.optimizers import Adam
from collections import deque
from actionspace import *
import tensorflow as tf



configproto = tf.compat.v1.ConfigProto() 
configproto.gpu_options.allow_growth = True
sess = tf.compat.v1.Session(config=configproto) 
tf.compat.v1.keras.backend.set_session(sess)



class DQNAgent:
    def __init__(self, learning_rate=0.001, epsilon=1.0, epsilon_decay=0.9975 , gamma=0.95):
        self.memory = deque(maxlen=10000)
        self.gamma = gamma    # discount rate
        self.epsilon = epsilon # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.training_history = None
        self.nr_actions = 56
        self.nr_states = 25

        self.map_actions_to_id = {
            'Recover': 0,
            'useRemains': 1,
            '1-1-1': 2, '1-1-2': 3, '1-1-3': 4, '1-1-4': 5, '1-1-5': 6, '1-1-6': 7,
            '1-2-1': 8, '1-2-2': 9, '1-2-3': 10, '1-2-4': 11, '1-2-5': 12, '1-2-6': 13,
            '1-3-1': 14, '1-3-2': 15, '1-3-3': 16, '1-3-4': 17, '1-3-5': 18, '1-3-6': 19,
            '2-1-1': 20, '2-1-2': 21, '2-1-3': 22, '2-1-4': 23, '2-1-5': 24, '2-1-6': 25,
            '2-2-1': 26, '2-2-2': 27, '2-2-3': 28, '2-2-4': 29, '2-2-5': 30, '2-2-6': 31,
            '2-3-1': 32, '2-3-2': 33, '2-3-3': 34, '2-3-4': 35, '2-3-5': 36, '2-3-6': 37,
            '3-1-1': 38, '3-1-2': 39, '3-1-3': 40, '3-1-4': 41, '3-1-5': 42, '3-1-6': 43,
            '3-2-1': 44, '3-2-2': 45, '3-2-3': 46, '3-2-4': 47, '3-2-5': 48, '3-2-6': 49,
            '3-3-1': 50, '3-3-2': 51, '3-3-3': 52, '3-3-4': 53, '3-3-5': 54, '3-3-6': 55
        }

        self.map_id_to_actions = {v: k for k, v in self.map_actions_to_id.items()}



        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        input_layer = Input(shape=(self.nr_states,))
        hidden_layer = Dense(40, activation='relu')(input_layer)
        output_layer = Dense(self.nr_actions, activation='softmax')(hidden_layer)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.learning_rate), metrics=['accuracy'])
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def step(self, input_state, action_list, actionspace, train):
        random_action = False
        if train:
            self.epsilon *= self.epsilon_decay
            self.epsilon = max(self.epsilon_min, self.epsilon)

            if np.random.random() < self.epsilon:
                output = action_list
                random_action = True
        #inputs = tf.expand_dims(input_state, 0)
        #output = self.model(inputs)[0].numpy()
        if random_action:
            action = random.choice(output)
            action_id = self.map_actions_to_id[action]
        else:
            input_state = tf.expand_dims(input_state, 0)
            output = self.model.predict(input_state, verbose=0)[0]
            legal_outputs = ReducePossibleActions(actionspace, output)
            action_id = np.argmax(legal_outputs)
            action = self.map_id_to_actions[action_id]

        return action, action_id

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size:
            return
        samples = random.sample(list(self.memory), batch_size)
        for sample in samples:
            input_state, action, reward, next_state, done = sample
            input_state = tf.expand_dims(input_state, 0) # make tensorflow tensor
            #target = self.target_model(inputs, training=True)[0].numpy()
            target = self.target_model.predict(input_state, verbose=0)[0]
            
            if done:
                target[action] = reward
            else:
                next_state = tf.expand_dims(next_state, 0)
                #Q_future = max(self.target_model(next_inputs, training=True)[0].numpy())
                Q_future = max(self.target_model.predict(next_state, verbose=0)[0])
                target[action] = reward + Q_future * self.gamma
                target = tf.expand_dims(target, 0)
                self.training_history = self.model.fit(input_state, target, epochs=1, verbose=0)
                
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

    