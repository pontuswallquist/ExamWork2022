import pygame
from cards import *
from player import Servant

colors = {
    'yellow': (255, 200, 0),
    'white': (255, 255, 255)
}

shortcardtypes = {
    1: 'R',
    2: 'I',
    3: 'J',
    4: 'M',
    5: 'P',
    6: 'T'
}

longcardtypes = {
    1: 'Remains',
    2: 'Idol',
    3: 'Jewelry',
    4: 'Manuscript',
    5: 'Pottery',
    6: 'Tapestry'
}

# Initialize Pygame
pygame.init()
# Set the window size
window_size = (1400, 800)
# Create the window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Crypt')
bg = pygame.image.load('images/Background.png')
bg_rect = bg.get_rect(topleft=(0,0))
screen.blit(bg, bg_rect)

#Dynamically draw the cards in a players collection
def drawCollection(color, cards):
    if not cards:
        return
    if color == 'Blue':
        start_x = 420
        start_y = 80
    elif color == 'Red':
        start_x = 460
        start_y = 665
    rects = []
    card_width = 30
    card_height = 40
    spacing = 5
    font = pygame.font.Font("consola.ttf", 24)
    y = start_y
    x = start_x
    for i, card in enumerate(cards):
        if i == 13:
            y = start_y + card_height + spacing
            x = start_x
        rects.append(pygame.Rect(x, y, card_width, card_height))
        pygame.draw.rect(screen, colors['white'], rects[i], 2)
        value_text = font.render(shortcardtypes[card.type], True, colors['yellow'])
        text_width, text_height = value_text.get_size()
        text_x = x + (card_width - text_width) / 2
        text_y = y + (card_height - text_height) / 2
        screen.blit(value_text, (text_x, text_y))
        x = x + card_width + spacing


def diceNumber(color, servant):
    if servant.value <= 1:
        servant_image = pygame.image.load(f'images/{color}One.png')
    elif servant.value == 2:
        servant_image = pygame.image.load(f'images/{color}Two.png')
    elif servant.value == 3:
        servant_image = pygame.image.load(f'images/{color}Three.png')
    elif servant.value == 4:
        servant_image = pygame.image.load(f'images/{color}Four.png')
    elif servant.value == 5:
        servant_image = pygame.image.load(f'images/{color}Five.png')
    elif servant.value == 6:
        servant_image = pygame.image.load(f'images/{color}Six.png')
    return servant_image
        
#Dynamically draw the servants available to a player
def drawServants(color, servants):
    if not servants:
        return
    if color == 'Blue':
        start_x = 90
        start_y = 90
    elif color == 'Red':
        start_x = 1050
        start_y = 670
    dice_width = 60
    dice_height = 60
    spacing = 25

    y = start_y
    x = start_x

    for i, servant in enumerate(servants):
        servant_image = diceNumber(color, servant)
        servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
        servant_rect = servant_image.get_rect(topleft=(x, y))
        screen.blit(servant_image, servant_rect)
        x = x + dice_width + spacing

def drawExhausted(color, servants):
    if not servants:
        return
    if color == 'Blue':
        start_x = 1010
        start_y = 90
    elif color == 'Red':
        start_x = 125
        start_y = 670
    dice_width = 60
    dice_height = 60
    spacing = 25

    y = start_y
    x = start_x

    for i, servant in enumerate(servants):
        servant_image = diceNumber(color, servant)
        servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
        servant_rect = servant_image.get_rect(topleft=(x, y))
        screen.blit(servant_image, servant_rect)
        
        x = x + dice_width + spacing

def drawBoard(board):

    cards = [board[i]['card'] for i in board.keys()]

    card_width, card_height = 200, 250
    card_spacing = 20
    font = pygame.font.Font("consola.ttf", 24)
     # Calculate the total width of the cards
    total_width = card_width * len(cards) + card_spacing * (len(cards) - 1)
    # Calculate the starting x position for the cards
    start_x = window_size[0] // 2 - total_width // 2


    for i, card in enumerate(cards):
        # Calculate the card position
        x = start_x + i * (card_width + card_spacing)
        y = window_size[1] // 2 - card_height // 2
        # Draw the card outline
        pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height), 2)
        # Draw the card value
        if i < 2:
            value_text = font.render(str(card.coinvalue), True, colors["yellow"])
            value_text_rect = value_text.get_rect()
            value_text_rect.center = (x + card_width // 2, y + card_height // 4)
            screen.blit(value_text, value_text_rect)
        # Draw the card type
        type_text = font.render(longcardtypes[card.type], True, colors["white"])
        type_text_rect = type_text.get_rect()
        type_text_rect.center = (x + card_width // 2, y + card_height * 2 // 4)
        screen.blit(type_text, type_text_rect)

    drawServantsOnBoard(board[1]['servants'], 1)
    drawServantsOnBoard(board[2]['servants'], 2)
    drawServantsOnBoard(board[3]['servants'], 3)



# Draw the servants on the board
def drawServantsOnBoard(servants, card_nr):
    if not servants:
        return
    if card_nr == 1:
        start_x, start_y = 385, 450
    elif card_nr == 2:
        start_x, start_y = 605, 450
    elif card_nr == 3:
        start_x, start_y = 825, 450
    spacing = 5
    dice_width = 60
    dice_height = 60

    x = start_x
    y = start_y

    for i, servant in enumerate(servants):
        servant_image = diceNumber(servant.color, servant)
        servant_image = pygame.transform.scale(servant_image, (dice_width, dice_height))
        servant_rect = servant_image.get_rect(topleft=(x, y))
        screen.blit(servant_image, servant_rect)
        
        x = x + dice_width + spacing

# Highlight selected rectangle
#redServant2_rect = redServant2.get_rect(topleft=redServantsPos[1])
#pygame.draw.rect(screen, colors['yellow'], redServant2_rect, 2)


def drawRecoverButton():
    width = 150
    height = 50
    x = 150
    y = 500
    font = pygame.font.Font("consola.ttf", 24)

    recoverButton_rect = pygame.draw.rect(screen, colors['white'], (x, y, width, height), 2)
    value_text = font.render('Recover', True, colors['yellow'])
    text_width, text_height = value_text.get_size()
    text_x = x + (width - text_width) / 2
    text_y = y + (height - text_height) / 2
    screen.blit(value_text, (text_x, text_y))

def drawUseRemains():
    width = 150
    height = 50
    x = 1150
    y = 500
    font = pygame.font.Font("consola.ttf", 24)

    useRemains_rect = pygame.draw.rect(screen, colors['white'], (x, y, width, height), 2)
    value_text = font.render('Use Remains', True, colors['yellow'])
    text_width, text_height = value_text.get_size()
    text_x = x + (width - text_width) / 2
    text_y = y + (height - text_height) / 2
    screen.blit(value_text, (text_x, text_y))


board = {
    1: {'card': TreasureCard(2, 4), 'servants': [Servant('Blue')] },
    2: {'card': TreasureCard(4, 2), 'servants': [] },
    3: {'card': TreasureCard(3, 1), 'servants': [] }
}

servantsRed = [Servant('Red'), Servant('Red'), Servant('Red')]
servantsBlue = [Servant('Blue'), Servant('Blue'), Servant('Blue')]
exhaustedBlue = []
exhaustedRed = []
collectcardsRed = [TreasureCard(1, 2), TreasureCard(5, 2), TreasureCard(6, 1)]
collectcardsBlue = [TreasureCard(3,2), TreasureCard(4,3), TreasureCard(2,2), TreasureCard(6,2)]


drawBoard(board)
drawServants('Blue', servantsBlue)
drawServants('Red', servantsRed)
drawExhausted('Red', exhaustedRed)
drawExhausted('Blue', exhaustedBlue)
drawCollection('Blue', collectcardsBlue)
drawCollection('Red', collectcardsRed)
drawRecoverButton()
drawUseRemains()
print(bg.get_alpha())
bg.fill((64,64,64))
bg.set_alpha(200)
screen.blit(bg, bg_rect)
print(bg.get_alpha())

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()