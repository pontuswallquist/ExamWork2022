from game import Crypt
from DQN_agent import DQNAgent
from rich.console import Console
from rich.progress import track
import tensorflow as tf
import numpy as np
import time



def trainNewAgent(nr_of_games, training_model_number, enemy_model_number):
    console = Console()
    avg_score = 0
    train = True
    log = False

    train_agent = DQNAgent()
    enemy_agent = DQNAgent(epsilon=0.2)
    enemy_agent.load_model(f'model_{enemy_model_number}.h5')

    writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_{training_model_number}")

    start = time.time()
    env = Crypt()
    for i in track(range(nr_of_games), description=f'Training agent {training_model_number}...'):
        
        env.playGame(enemy_agent, train_agent, train, log)
        # Train target network every 5 games
        if i % 5 == 0 and i > 2:
            train_agent.target_train()
        #avg_score += state.players[1].score
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

    

def ContinueTraining(training_model_number, enemy_model_number, start_game, end_game):
    console = Console()
    avg_score = 0
    train = True
    log = False

    train_agent = DQNAgent()
    train_agent.load_model(f'model_{training_model_number}.h5')
    train_agent.load_target_model(f'target_model_{training_model_number}.h5')

    with open(f'parameters_{training_model_number}.txt', 'r') as f:
        train_agent.epsilon = float(f.readline())
        train_agent.gamma = float(f.readline())
        train_agent.learning_rate = float(f.readline())
    

    enemy_agent = DQNAgent(epsilon=0.01)
    enemy_agent.load_model(f'model_{enemy_model_number}.h5')

    writer = tf.summary.create_file_writer(logdir=f"tensorboard/model_1_200")

    start = time.time()
    env = Crypt()
    for i in range(start_game, end_game):  #track(range(start_game, end_game), description=f'Training agent {training_model_number}...'):
        
        env.playGame(enemy_agent, train_agent, train, log)
        
        #avg_score += env.players[1].score
        if i > start_game + 2:
            with writer.as_default():
                tf.summary.scalar("Score each game", env.players[1].score, step=i)
                tf.summary.scalar("Enemy score each game", env.players[0].score, step=i)
                tf.summary.scalar("Epsilon each game", train_agent.epsilon, step=i)
                tf.summary.scalar("Loss ", np.average(train_agent.training_history.history['loss']), step=i)
                tf.summary.scalar("Accuracy", np.average(train_agent.training_history.history['accuracy']), step=i)
        env.reset()
    
    end = time.time()
    console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")


    model_nr = training_model_number.split('_')[0]

    train_agent.save_model(f'model_{model_nr}_{end_game}.h5')
    train_agent.save_target_model(f'target_model_{model_nr}_{end_game}.h5')

    with open(f'parameters_{model_nr}_{end_game}.txt', 'w') as f:
        f.write(f'{train_agent.epsilon}\n{train_agent.gamma}\n{train_agent.learning_rate}\n')

    del train_agent
    del enemy_agent
    

trainNewAgent(2000, 13, 14)





