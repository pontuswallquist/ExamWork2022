import crypt

gamestate = crypt.Crypt()
game_over = False
while not game_over:
    gamestate.revealphase()
    gamestate.claimphase()
    gamestate.collectphase()
    game_over = gamestate.passTorchphase(game_over)

