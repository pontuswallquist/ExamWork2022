from gamephases import *

from rich.layout import Layout
from rich import print
from rich.panel import Panel
from rich.align import Align

state = crypt.Crypt()
state = revealPhase(state)

layout = Layout()
layout.split_column(
    Layout(name="Crypt"),
    Layout(name="Players"),
    Layout(name="Input")
)


layout["Crypt"].split_row(
    Layout(name="Place1"),
    Layout(name="Place2"),
    Layout(name="Place3")
)

layout['Place1'].split_column(
    Layout(Align.center(Panel(str(state.board[1]['card']), title="Card 1")), name="Card1"),
    Layout(Align.center(Panel(str(state.board[1]['servants']), title="Servants")), name="Servants1")
)

layout['Place2'].split_column(
    Layout(Align.center(Panel(str(state.board[2]['card']), title="Card 2")), name="Card2"),
    Layout(Align.center(Panel(str(state.board[2]['servants']), title="Servants")), name="Servants2")
)

layout['Place3'].split_column(
    Layout(Align.center(Panel(str(state.board[3]['card']), title="Card 3")), name="Card3"),
    Layout(Align.center(Panel(str(state.board[3]['servants']), title="Servants")), name="Servants3")
)

layout["Players"].split_row(
    Layout(name="Red"),
    Layout(name="Blue")
)

layout["Red"].split_column(
    Layout(Align.center(Panel(str(state.players[0].servants), title="Red Servants")), name="RedServants"),
    Layout(Align.center(Panel(str(state.players[0].collection), title="Red Treasures")),name="RedTreasures")
)

layout["Blue"].split_column(
    Layout(Align.center(Panel(str(state.players[1].servants), title="Blue Servants")), name="BlueServants"),
    Layout(Align.center(Panel(str(state.players[1].collection), title="Blue Treasures")),name="BlueTreasures")
)

#layout["Crypt"].update(state)

print(layout)