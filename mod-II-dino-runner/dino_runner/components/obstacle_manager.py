from dino_runner.components.obstacles.obstacle import Obstacle
from dino_runner.components.obstacles.small_cactus import Cactus
from dino_runner.components.obstacles.birds import Bird
from dino_runner.utils.constants import HAMMER
from dino_runner.utils.constants import DINO_DEATH, RESET, SCREEN_HEIGHT, SCREEN_WIDTH, SHIELD_TYPE, HAMMER_TYPE
import random
import pygame
import time

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.image = DINO_DEATH
        self.obstacle_types = {
            0: {'type': 'Cactus', 'size': 'SMALL'},
            1: {'type': 'Cactus', 'size': 'LARGE'},
            2: {'type': 'Bird'}
        }
        self.bullets = pygame.sprite.Group()
        self.bullet_image = pygame.image.load('dino_runner/assets/Other/hammer.png')
        self.bullet_speed = 10
        self.bullet_start_time = None
        self.bullet_lifetime = 1.0

    def generate_obstacle(self, obstacle_type):
        obstacle_params = self.obstacle_types[obstacle_type]
        if obstacle_params['type'] == 'Cactus':
            obstacle = Cactus(obstacle_params['size'])
        else:
            obstacle = Bird()
        return obstacle

    def update(self, game, user_input):
        if not self.obstacles:
            obstacle_type = random.randint(0, 2)
            obstacle = self.generate_obstacle(obstacle_type)
            self.obstacles.append(obstacle)

        for obstacle in self.obstacles:
            remove2 = game.player.rect.colliderect(obstacle.rect)
            obstacle.update(game.game_speed, self.obstacles)

        if game.player.type == SHIELD_TYPE and remove2:
            game.playing = True
            self.obstacles.remove(obstacle)

        else:
            if remove2:
                game.lives -= 1
                if game.lives == 0:
                    game.playing = False
                else:
                    self.obstacles.remove(obstacle)

        if game.player.type == HAMMER_TYPE and user_input[pygame.K_SPACE]:
            bullet = HAMMER(self.bullet_image, game.player.rect.right, game.player.rect.centery)
            self.bullets.add(bullet)
            self.bullet_start_time = time.time()

        for bullet in self.bullets:
            bullet.update()
            if time.time() - self.bullet_start_time > self.bullet_lifetime:
                self.bullets.remove(bullet)
            else:
                for obstacle in self.obstacles:
                    if bullet.rect.colliderect(obstacle.rect):
                        self.obstacles.remove(obstacle)
                        self.bullets.remove(bullet)
                        break



    def check_game_status(self,game):
        if game.lives <= 0:
            game.playing = False
            return
        for obstacle in self.obstacles:
            if game.player.rect.colliderect(obstacle.rect):
                game.player.lives -= 1  # restar una vida al jugador
                if game.player.lives <= 0:
                    game.playing = False
                return

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
        for bullet in self.bullets:
            bullet.draw(screen)

    def remove_obstacle(self):
        self.obstacles=[]


class HAMMER(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.right = x_pos
        self.rect.centery = y_pos
        self.speed = 20
        self.lifespan = 60 # tiempo de vida en frames

    def update(self):
        self.rect.x += self.speed
        self.lifespan -= 1  # restar tiempo de vida
        if self.lifespan <= 0:
            self.kill()
    def draw(self, screen):
        screen.blit(self.image, self.rect)