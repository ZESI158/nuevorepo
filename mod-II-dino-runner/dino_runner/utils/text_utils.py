import pygame
from dino_runner.utils.constants import SCREEN_HEIGHT, SCREEN_WIDTH, FONT_STYLE, RESET
FONT_STYLE = FONT_STYLE
BLACK_COLOR = (0,0,0)
WHITE_COLOR = (255,255,255)



def get_center_message(message):
    font = pygame.font.Font(FONT_STYLE, 30)
    text = font.render(message, True, WHITE_COLOR)
    rect = text.get_rect()
    rect.center = (SCREEN_WIDTH // 2,400)
    return text, rect
def get_center_message_game(message):
    font = pygame.font.Font(FONT_STYLE, 30)
    text = font.render(message, True, BLACK_COLOR)
    rect = text.get_rect()
    rect.center = (SCREEN_WIDTH // 2, 350)
    return text, rect

