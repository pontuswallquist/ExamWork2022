from game import Crypt
from DQN_agent import DQNAgent
from player import RandomPlayer, HumanPlayer
from rich.console import Console
from rich.progress import track
import tensorflow as tf
import numpy as np
import time



def trainNewAgent(training_model_number, enemy_type, nr_of_games):
    console = Console()
    train = True
    log = False

    if enemy_type == 'random':
        enemy_agent = RandomPlayer('Red', torch=True)
    elif enemy_type == 'human':
        enemy_agent = HumanPlayer('Red', torch=True)
    else:
        enemy_agent = DQNAgent('Red', torch=True, epsilon=0.01)
        enemy_agent.load_model(f'model_{enemy_type}.h5')

    train_agent = DQNAgent('Blue')

    writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_{training_model_number}")

    start = time.time()
    env = Crypt(enemy_agent, train_agent)
    for i in track(range(nr_of_games), description=f'Training agent {training_model_number}...'):
        
        env.playGame(train, log)
        # Train target network every 20 games
        if i % 25 == 0 and i > 0:
            train_agent.target_train()
        if i > 2:
            with writer.as_default():
                tf.summary.scalar("Score each game", env.players[1].score, step=i)
                tf.summary.scalar("Enemy score each game", env.players[0].score, step=i)

                tf.summary.scalar("Epsilon each game", train_agent.epsilon, step=i)
                tf.summary.scalar("Loss ", np.average(train_agent.training_history.history['loss']), step=i)
                tf.summary.scalar("Accuracy", np.average(train_agent.training_history.history['accuracy']), step=i)
        env.reset()
    
    end = time.time()
    console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")

    train_agent.save_model(f'model_{training_model_number}.h5')
    train_agent.save_target_model(f'target_model_{training_model_number}.h5')
    # save all other attributes to a file
    with open(f'parameters_{training_model_number}.txt', 'w') as f:
        f.write(f'{train_agent.epsilon}\n{train_agent.gamma}\n{train_agent.learning_rate}\n')

    del train_agent
    del enemy_agent




trainNewAgent(26, 23, 1000)







