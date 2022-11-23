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



def testAgent(model_number, nr_of_games):
    train = False
    train_target = False
    log = False
    agent = DQNAgent(epsilon=0.01)
    agent.load_model(f'model_{model_number}.h5')
    model_wins = []
    random_wins = []
    ties = []
    for i in range(nr_of_games):
        state = Crypt()
        train_target = False
        state = playGame(state, agent, train, train_target, log)
        append_winner(state, model_wins, random_wins, ties)
        del state
    console.print(f"Model {model_number} won {len(model_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_number} lost {len(random_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_number} tied {len(ties)/nr_of_games*100}% of the games")
    
def playSingleGame(model_number):
    train = False
    train_target = False
    log = True
    agent = DQNAgent(epsilon=0.01)
    agent.load_model(f'model_{model_number}.h5')
    state = Crypt()
    train_target = False
    state = playGame(state, agent, train, train_target, log)
    print("Done!")

    
#testAgent(7, 250)
playSingleGame(7)


