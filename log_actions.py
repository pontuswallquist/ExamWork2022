from rich.console import Console

def log_action(state, action, playernr):
    if playernr == 0:
        justified = 'left'
    else:
        justified = 'right'

    with open('game_log.txt', 'a') as f:
        console = Console(file=f)
        console.print('Board:', justify=justified)
        console.print(state.board[1]['card'], state.board[1]['servants'], justify=justified)
        console.print(state.board[2]['card'], state.board[2]['servants'], justify=justified)
        console.print(state.board[3]['card'], state.board[3]['servants'], justify=justified)
        console.print('')
        console.print('Player', playernr, justify=justified)
        console.print('Servants:', state.players[playernr].nr_servants_available(), justify=justified)
        console.print(state.players[playernr].collection, justify=justified)
        console.print('Action: ', action, justify=justified)
        console.print('============================', justify=justified)






