from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
console = Console()

def append_winner(state, model_wins, random_wins, ties):
    if state.players[0].score > state.players[1].score:
        model_wins.append((state.players[0].score, state.players[1].score))
    elif state.players[0].score < state.players[1].score:
        random_wins.append((state.players[1].score, state.players[0].score))
    else:
        ties.append(state.players[0].score)




train = False
train_target = False
nr_of_games = 200
agent = DQNAgent()
agent.load_model('model_2.h5')
model_wins = []
random_wins = []
ties = []

for i in range(nr_of_games):
    state = Crypt()
    state = playGame(state, agent, train, train_target)
    console.print('[bold green]Game: ', i, justify='center')
    append_winner(state, model_wins, random_wins, ties)
    del state

console.print(f"Model wins: {len(model_wins)}")
console.print(f"Model win percentage: {(len(model_wins)/nr_of_games)*100} %")

console.print(f"Random wins: {len(random_wins)}")
console.print(f"Random win percentage: {(len(random_wins)/nr_of_games)*100} %")

console.print(f"Ties: {len(ties)}")
