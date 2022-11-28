from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
from rich.progress import track
import tensorflow as tf
import numpy as np
import time



def trainNewAgent(nr_of_games, training_model_number, learning_rate, gamma):
    console = Console()
    avg_score = 0
    train = True
    log = False

    train_agent = DQNAgent(learning_rate=learning_rate, epsilon_decay=0.9975, gamma=gamma)

    # vs Random agent
    #enemy_agent = DQNAgent(epsilon=0.01)
    #enemy_agent.load_model(f'model_{enemy_model_number}.h5')

    #writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_{training_model_number}")

    start = time.time()
    for i in track(range(nr_of_games), description=f'Training agent {training_model_number}...'):
        state = Crypt()
        state = playGame(state, train_agent, train, log)
        avg_score += state.players[1].score
        #if i > 2:
        #    with writer.as_default():
        #        tf.summary.scalar("Score each game", state.players[1].score, step=i)
        #        tf.summary.scalar("Epsilon each game", train_agent.epsilon, step=i)
        #        tf.summary.scalar("Loss ", np.average(train_agent.training_history.history['loss']), step=i)
        #        tf.summary.scalar("Accuracy", np.average(train_agent.training_history.history['accuracy']), step=i)
        del state
    
    end = time.time()
    console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")

    train_agent.save_model(f'model_{training_model_number}.h5')
    train_agent.save_target_model(f'target_model_{training_model_number}.h5')
    # save all other attributes to a file
    parameters = np.array([train_agent.epsilon, train_agent.gamma, train_agent.learning_rate])
    np.savetxt(f'parameters_{training_model_number}.txt', parameters)

    del train_agent
    #del enemy_agent

    

def continueTraining(nr_of_games, training_model_number):
    console = Console()
    avg_score = 0
    train = True
    log = False

    train_agent = DQNAgent()
    train_agent.load_model(f'model_{training_model_number}.h5')
    train_agent.load_target_model(f'target_model_{training_model_number}.h5')

    train_agent.epsilon, train_agent.gamma, train_agent.learning_rate = np.loadtxt(f'parameters_{training_model_number}.txt', unpack=True)
    

    #enemy_agent = DQNAgent(epsilon=0.01)
    #enemy_agent.load_model(f'model_{enemy_model_number}.h5')

    writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_{training_model_number}")

    start = time.time()
    for i in track(range(nr_of_games), description=f'Training agent {training_model_number}...'):
        state = Crypt()
        state = playGame(state, train_agent, train, log)
        avg_score += state.players[1].score
        if i > 2:
            with writer.as_default():
                tf.summary.scalar("Score each game", state.players[1].score, step=i)
                tf.summary.scalar("Epsilon each game", train_agent.epsilon, step=i)
                tf.summary.scalar("Loss ", np.average(train_agent.training_history.history['loss']), step=i)
                tf.summary.scalar("Accuracy", np.average(train_agent.training_history.history['accuracy']), step=i)
        del state
    
    end = time.time()
    console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")

    train_agent.save_model(f'model_{training_model_number}.h5')
    train_agent.save_target_model(f'target_model_{training_model_number}.h5')

    parameters = np.array([train_agent.epsilon, train_agent.gamma, train_agent.learning_rate])
    np.savetxt(f'parameters_{training_model_number}.txt', parameters)

    del train_agent
    #del enemy_agent



trainNewAgent(100, 1, 0.002, 0.85)

continueTraining(100, 1)

continueTraining(100, 1)

print("Done")

