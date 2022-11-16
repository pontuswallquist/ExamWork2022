from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
import time
console = Console()


train = True
nr_of_games = 100
agent = DQNAgent()

start = time.time()
for i in range(nr_of_games):
    state = Crypt()
    train_target = True
    state = playGame(state, agent, train, train_target)
    console.print('[bold green]Game: ', i, justify='center')
    del state
    
end = time.time()

console.print(f"Time: {int((end-start)/3600)} hours and {int(((end-start)%3600)/60)} minutes")

agent.save_model('model_2.h5')
