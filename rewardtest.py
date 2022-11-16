from crypt import Crypt
from cards import *


game = Crypt()

game.updateNewBoard(1)
game.updateNewBoard(2)
game.updateNewBoard(3)

game.players[0].collection.append(TreasureCard(1, 2))
game.players[0].collection.append(TreasureCard(2, 1))
game.players[0].collection.append(TreasureCard(3, 4))
game.players[0].collection.append(TreasureCard(1, 4))
game.players[0].collection.append(TreasureCard(4, 4))
game.players[0].collection.append(TreasureCard(5, 4))
game.players[0].collection.append(TreasureCard(5, 3))
game.players[0].collection.append(TreasureCard(5, 2))
game.players[0].collection.append(TreasureCard(6, 4))
game.players[0].collection.append(TreasureCard(5, 1))

#game.players[0].turnAllCards()

print(game.players[0].collection)

print(game.get_input_state(0))


