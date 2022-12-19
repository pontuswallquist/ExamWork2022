import pygame

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (1600, 800)

# Create the window
screen = pygame.display.set_mode(window_size)

# Set the card size and spacing
card_width, card_height = 200, 300
card_spacing = 20

# Set the font and text color
font = pygame.font.Font(None, 36)
text_color = (255, 255, 255)

# Set the cards
cards = [
    {"value": "A", "type": "Spades"},
    {"value": "2", "type": "Hearts"},
    {"value": "Q", "type": "Diamonds"},
]

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Calculate the total width of the cards
    total_width = card_width * len(cards) + card_spacing * (len(cards) - 1)

    # Calculate the starting x position for the cards
    start_x = window_size[0] // 2 - total_width // 2

    # Draw the cards
    for i, card in enumerate(cards):
        # Calculate the card position
        x = start_x + i * (card_width + card_spacing)
        y = window_size[1] // 2 - card_height // 2

        # Draw the card outline
        pygame.draw.rect(screen, (255, 255, 255), (x, y, card_width, card_height), 2)

        # Draw the card value
        value_text = font.render(card["value"], True, text_color)
        value_text_rect = value_text.get_rect()
        value_text_rect.center = (x + card_width // 2, y + card_height // 4)
        screen.blit(value_text, value_text_rect)

        # Draw the card type
        type_text = font.render(card["type"], True, text_color)
        type_text_rect = type_text.get_rect()
        type_text_rect.center = (x + card_width // 2, y + card_height * 3 // 4)
        screen.blit(type_text, type_text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()