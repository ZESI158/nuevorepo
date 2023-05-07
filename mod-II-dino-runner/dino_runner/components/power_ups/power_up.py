import random
from pygame.sprite import Sprite
from dino_runner.utils.constants import SCREEN_WIDTH

class Power_Up(Sprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(150,180)
        self.start_time = 0

    def update(self, game_speed):
        self.rect.x -= game_speed



    def draw(self, screen):
        screen.blit(self.image, self.rect)