from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.utils.constants import SHIELD, DEFAULT_TYPE, HAMMER, HEARTH
from dino_runner.components.power_ups.hearth import Hearth

import random
import pygame


class PowerUpManager:
    POWER_UP_PROBABILITY = 100
    POWER_UP_CLASSES = {
        SHIELD: Shield,
        HAMMER: Hammer,
        HEARTH: Hearth,
    }

    def __init__(self):
        self.power_ups = []
        

    def generate_power_up(self):
        if random.randint(0, 1000) < self.POWER_UP_PROBABILITY:
            random_type = random.choice(list(self.POWER_UP_CLASSES.keys()))
            if not any(isinstance(p, self.POWER_UP_CLASSES[random_type]) for p in self.power_ups):
                power_up = self.POWER_UP_CLASSES[random_type](random_type)
                self.power_ups.append(power_up)

    def update(self, game):
        if len(self.power_ups) == 0 and game.player.type == DEFAULT_TYPE:
            self.generate_power_up()

        for power_up in self.power_ups:
            power_up.update(game.game_speed)

            if power_up.rect.x < -power_up.rect.width:
                self.power_ups.remove(power_up)

            if game.player.rect.colliderect(power_up.rect):
                if isinstance(power_up, Hearth):  # si es un power_up de tipo Hearth
                    game.increment_lives()  # aumentar las vidas del juego
                else:
                    game.player.active_power_up(power_up.type)
                self.power_ups.remove(power_up)
    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def remove_powers(self):
        self.power_ups = []
