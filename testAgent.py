from crypt import Crypt
from DQN_agent import DQNAgent
from NpcVsNpc import playGame
from rich.console import Console
from rich.progress import track
console = Console()

def append_winner(state, model1_wins, model2_wins, ties):
    if state.players[1].score > state.players[0].score:
        model1_wins.append((state.players[1].score, state.players[0].score))
    elif state.players[1].score < state.players[0].score:
        model2_wins.append((state.players[1].score, state.players[0].score))
    else:
        ties.append(state.players[1].score)



def testAgent(enemy_model_number, trained_model_number, nr_of_games):
    train = False
    log = False

    enemy_agent = DQNAgent(epsilon=0.01)
    enemy_agent.load_model(f'model_{enemy_model_number}.h5')

    trained_agent = DQNAgent(epsilon=0.01)
    trained_agent.load_model(f'model_{trained_model_number}.h5')

    trained_model_wins = []
    enemy_model_wins = []
    ties = []
    avg_score = 0

    for i in track(range(nr_of_games), description=f'Testing agent {trained_model_number}...'):
        state = Crypt()
        state = playGame(state, enemy_agent, trained_agent, train, log)
        avg_score += state.players[1].score
        append_winner(state, trained_model_wins, enemy_model_wins, ties)
        del state
    console.print(f"Model {trained_model_number} won {len(trained_model_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {trained_model_number} lost {len(enemy_model_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {trained_model_number} tied {len(ties)/nr_of_games*100}% of the games")
    console.print(f"Model {trained_model_number} average score: {avg_score/nr_of_games}")
    
def playSingleGame(enemy_model_number, trained_model_number):
    train = False
    log = True
    enemy_agent = DQNAgent(epsilon=0.01)
    enemy_agent.load_model(f'model_{enemy_model_number}.h5')
    trained_agent = DQNAgent(epsilon=0.01)
    trained_agent.load_model(f'model_{trained_model_number}.h5')
    state = Crypt()
    state = playGame(state, enemy_agent, trained_agent, train, log)
    print("Done!")

    
playSingleGame(13, 14)




