from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame



train = True
nr_of_games = 10
agent = DQNAgent()

for i in range(nr_of_games):
    state = Crypt()
    train_target = True
    state = playGame(state, agent, train, train_target)
    print('Game: ', i)
    state.printTrainScore()
    del state
    
agent.save_model('model_1')

