from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
from rich.progress import track
import tensorflow as tf
import numpy as np
import time



def trainAgent(nr_of_games, model_number, learning_rate, gamma):
    console = Console()
    avg_score = 0
    train = True
    log = False
    agent = DQNAgent(learning_rate=learning_rate, epsilon_decay=0.9975, gamma=gamma)

    writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_{model_number}")

    start = time.time()
    for i in track(range(nr_of_games), description=f'Training agent {model_number}...'):
        state = Crypt()
        state = playGame(state, agent, train, log)
        avg_score += state.players[0].score
        if i > 2:
            with writer.as_default():
                tf.summary.scalar("Score each game", state.players[0].score, step=i)
                tf.summary.scalar("Epsilon each game", agent.epsilon, step=i)
                tf.summary.scalar("Loss ", np.average(agent.training_history.history['loss']), step=i)
                tf.summary.scalar("Accuracy", np.average(agent.training_history.history['accuracy']), step=i)
        del state
    
    end = time.time()
    console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")

    agent.save_model(f'model_{model_number}.h5')
#Write model info to file
    with open('model-logger.txt', 'a') as f:
        f.write('\n')
        f.write(f'model_{model_number}\n')
        f.write(f"Trained for {nr_of_games} games\n")
        f.write(f"Learning rate: {agent.learning_rate}\n")
        f.write(f"Epsilon decay: {agent.epsilon_decay}\n")
        f.write(f"Gamma: {agent.gamma}\n")
        f.write(f"Average score: {avg_score/nr_of_games}\n")
        
        


trainAgent(500, 15, 0.002, 0.85)





