from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
console = Console()

def get_score_and_winner(state):
    if state.players[0].score > state.players[1].score:
        winner = 'Model'
    elif state.players[0].score < state.players[1].score:
        winner = 'Random'
    else:
        winner = 'Tie'

    return f"Model: {state.players[0].score} Random: {state.players[1].score} Winner: {winner}"



train = True
nr_of_games = 5
agent = DQNAgent()
game_scores = []

for i in range(nr_of_games):
    state = Crypt()
    train_target = True
    state = playGame(state, agent, train, train_target)
    console.print('[bold green]Game: ', i, justify='center')
    game_scores.append(get_score_and_winner(state))
    del state
    
console.print(game_scores, justify='left')
agent.save_model('model_1.h5')
