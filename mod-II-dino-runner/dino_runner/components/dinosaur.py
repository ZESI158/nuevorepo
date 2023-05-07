import pygame
from pygame.sprite import Sprite
from dino_runner.utils.constants import RUNNING, DUCKING, JUMPING, SCREEN_HEIGHT, SCREEN_WIDTH, DINO_DEATH
from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, RUNNING_SHIELD, JUMPING_SHIELD ,DUCKING_SHIELD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, HAMMER_TYPE, HEARTH, HEARTH_TYPE, RUNNING_HEARTH, JUMPING_HEARTH, DUCKING_HEARTH

RUN_IMG =  {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER, HEARTH_TYPE: RUNNING_HEARTH}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER, HEARTH_TYPE: JUMPING_HEARTH }
DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER, HEARTH_TYPE: DUCKING_HEARTH}
class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5
    POWER_UP_TIME = 100

    def __init__(self):
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.type = DEFAULT_TYPE
        self.image = RUN_IMG[self.type][0]  
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.power_up_time = 0
   

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

        self.power_up_time -=1
        if self.power_up_time <= 0:
            self.type = DEFAULT_TYPE


    def duck(self):
        self.image = DUCK_IMG[self.type][self.step_index // 5 ] 
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = RUN_IMG[self.type][ self.step_index // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        JUMP_IMG[self.type]
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
    
    def move_to_origin(self):
        self.image = RUNNING[0]
        self.step_index = 0
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = DEFAULT_TYPE

    def active_power_up(self, power_up_type):
        if power_up_type == SHIELD_TYPE:
            self.type = SHIELD_TYPE
            self.power_up_time = self.POWER_UP_TIME
        if power_up_type == HAMMER_TYPE:
            self.type = HAMMER_TYPE
            self.power_up_time = self.POWER_UP_TIME
        if power_up_type == HEARTH_TYPE:
            self.type = HEARTH_TYPE
            self.power_up_time = self.POWER_UP_TIME
    