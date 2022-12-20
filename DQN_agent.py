import numpy as np
import random
from player import PlayerInterface
from keras.layers import Input, Dense, Dropout
from keras import backend as K
from keras.models import Model, load_model
from keras.callbacks import Callback
from keras.optimizers import Adam
from collections import deque
import tensorflow as tf

def makeActionSpace1D(actionspace):
    actionspace1D = []
    actionspace1D.extend(actionspace[0])
    actionspace1D.extend(actionspace[1])
    actionspace1D.extend(actionspace[2])
    actionspace1D.extend(actionspace[3])
    return actionspace1D

def ReducePossibleActions(actionspace, actions):
    actionspace1d = makeActionSpace1D(actionspace)
    for i in range(len(actionspace1d)):
        actions[i] = actions[i] * actionspace1d[i]
    return actions

class ClearMemory(Callback):
    def on_epoch_end(self, epoch, logs=None):
        K.clear_session()

class DQNAgent(PlayerInterface):
    def __init__(self, color, torch=False, epsilon=1.0):
        super().__init__(color, torch)


        self.memory = deque(maxlen=10000)
        self.gamma = 0.85    # discount rate
        self.epsilon = epsilon # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.999
        self.learning_rate = 0.0025
        self.training_history = None
        self.nr_actions = 56
        self.nr_inputs = 25

        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        input_layer = Input(shape=(self.nr_inputs,))
        hidden_layer = Dense(40, activation='relu', kernel_initializer='he_uniform')(input_layer)
        output_layer = Dense(self.nr_actions, activation='linear', kernel_initializer='he_uniform')(hidden_layer)

        model = Model(inputs=input_layer, outputs=output_layer, name='DQN')

        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=self.learning_rate), metrics=['accuracy'])
        model.summary()
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
        
        if random_action:
            action = random.choice(output)
            action_id = self.map_actions_to_id[action]
        else:
            input_state = tf.expand_dims(input_state, 0)
            #output = self.model(input_state)[0].numpy()
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
            input_state = tf.expand_dims(input_state, 0) # makes tensorflow tensor
            #target = self.target_model(input_state, training=True)[0].numpy()
            target = self.target_model.predict(input_state, verbose=0)[0]
            
            if done:
                target[action] = reward
            else:
                next_state = tf.expand_dims(next_state, 0)
                #Q_future = max(self.target_model(next_state, training=True)[0].numpy())
                Q_future = max(self.target_model.predict(next_state, verbose=0)[0])
                target[action] = reward + Q_future * self.gamma
                target = tf.expand_dims(target, 0)
                self.training_history = self.model.fit(input_state, target, epochs=1, verbose=0, callbacks=ClearMemory())
                
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

    #save and load target model
    def save_target_model(self, file_name):
        self.target_model.save(file_name)

    def load_target_model(self, file_name):
        self.target_model = load_model(file_name)


    