from game import Crypt
from DQN_agent import DQNAgent
from player import RandomPlayer, HumanPlayer
from rich.console import Console
from rich.progress import track


def append_winner(state, model1_wins, model2_wins, ties):
    if state.players[1].score > state.players[0].score:
        model1_wins.append((state.players[1].score, state.players[0].score))
    elif state.players[1].score < state.players[0].score:
        model2_wins.append((state.players[1].score, state.players[0].score))
    else:
        ties.append(state.players[1].score)


def testModelVsModel(model_nr, enemy_nr, nr_of_games):
    train = False
    log = False
    console = Console()

    player1 = DQNAgent('Red', torch=True, epsilon=0.01)
    player1.load_model(f'model_{enemy_nr}.h5')

    player2 = DQNAgent('Blue', epsilon=0.01)
    player2.load_model(f'model_{model_nr}.h5')
    
    model_wins = []
    enemy_wins = []
    ties = []
    model_score = 0
    enemy_score = 0

    env = Crypt(player1, player2)
    for i in track(range(nr_of_games), description=f'Testing agent {model_nr}...'):
        
        env.playGame(train, log)
        enemy_score += env.players[0].score
        model_score += env.players[1].score
        append_winner(env, model_wins, enemy_wins, ties)
        player1.resetScore()
        player2.resetScore()
        env.reset()

    
    avg_model_score = model_score/nr_of_games
    avg_enemy_score = enemy_score/nr_of_games

    console.print(f"Model {model_nr} won {len(model_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} lost {len(enemy_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} tied {len(ties)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} average score: {avg_model_score}")
    console.print(f"Enemy {enemy_nr} average score: {avg_enemy_score}")

def testModelVsRandom(model_nr, nr_of_games):
    train = False
    log = False
    console = Console()

    player1 = RandomPlayer('Red', torch=True)

    player2 = DQNAgent('Blue', epsilon=0.01)
    player2.load_model(f'model_{model_nr}.h5')
    
    model_wins = []
    enemy_wins = []
    ties = []
    model_score = []
    enemy_score = []

    env = Crypt(player1, player2)
    for i in track(range(nr_of_games), description=f'Testing agent {model_nr}...'):
        
        env.playGame(train, log)
        enemy_score.append(env.players[0].score)
        model_score.append(env.players[1].score)
        append_winner(env, model_wins, enemy_wins, ties)
        player1.score = 0
        player2.score = 0
        env.reset()

    console.print(f"Model {model_nr} won {len(model_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} lost {len(enemy_wins)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} tied {len(ties)/nr_of_games*100}% of the games")
    console.print(f"Model {model_nr} average score: {(sum(model_score)/nr_of_games)}")
    console.print(f"Random average score: {(sum(enemy_score)/nr_of_games)}")
    
def singleGameModelVsModel(enemy_model_number, trained_model_number):
    train = False
    log = True
    console = Console()

    player1 = DQNAgent('Red', torch=True, epsilon=0.01)
    player1.load_model(f'model_{enemy_model_number}.h5')

    player2 = DQNAgent('Blue', epsilon=0.01)
    player2.load_model(f'model_{trained_model_number}.h5')

    env = Crypt(player1, player2)
    env.playGame(train, log)
    console.print(f"Model score: {env.players[1].score}")
    console.print(f"Enemy score: {env.players[0].score}")
    print("Done!")

def singleGameModelVsRandom(trained_model_number):
    train = False
    log = True
    console = Console()

    player1 = RandomPlayer('Red', torch=True)
    
    player2 = DQNAgent('Blue', epsilon=0.01)
    player2.load_model(f'model_{trained_model_number}.h5')

    env = Crypt(player1, player2)
    env.playGame(train, log)
    console.print(f"Model score: {env.players[1].score}")
    console.print(f"Enemy score: {env.players[0].score}")
    print("Done!")

def singleGameRandomVsRandom():
    train = False
    log = True

    player1 = RandomPlayer('Red', torch=True)
    player2 = RandomPlayer('Blue')

    env = Crypt(player1, player2)
    env.playGame(train, log)
    print("Done!")

def singleGameHumanVsModel(model_nr):
    train = False
    log = False

    player1 = HumanPlayer('Red', torch=True)
    player2 = DQNAgent('Blue', epsilon=0.01)
    player2.load_model(f'model_{model_nr}.h5')

    env = Crypt(player1, player2)
    env.playGame(train, log)
    print("Done!")


#testModelVsRandom(18, 100)

#testModelVsModel(18, 15, 100)









