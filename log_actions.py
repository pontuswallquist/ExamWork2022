from rich.console import Console

def log_action(state, action, playernr):
    if playernr == 0:
        justified = 'left'
    else:
        justified = 'right'

    with open('game_log.txt', 'a') as f:
        console = Console(file=f)
        console.print('Board:', justify=justified)
        console.print(state[0:2], state[2], justify=justified)
        console.print(state[3:4], state[5], justify=justified)
        console.print(state[6], state[7], justify=justified)
        console.print('')
        console.print('Player', playernr, justify=justified)
        console.print('Servants:', state.players[playernr].nr_servants_available(), justify=justified)
        console.print(state.players[playernr].collection, justify=justified)
        console.print('Action: ', action, justify=justified)
        console.print('============================', justify=justified)






