import pygame
import random
import time
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAME_SPEED, RESET, GAME_OVER,DINO_DEATH, HEARTH
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.utils.text_utils import  get_center_message, get_center_message_game
from dino_runner.components.cloud import Cloud
from dino_runner.components.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups_manager import PowerUpManager
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class Game:
    GAME_SPEED = 20
    colors = [(255, 255, 255),(0,0,0)]
    WHITE_COLOR = (255,255,255)
    color_background = colors[0]
    BLACK_COLOR = (0,0,0)
    pos_lifes = (10,15)
    heart_pos = (10,450)
    pos_score = (900,15)
    pos_highscore = (700,15)
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.player = Dinosaur()
        self.points = 0
        self.death_count = 0
        self.power_up_manager = PowerUpManager()
        self.highest_score = 0
        self.cloud = Cloud()
        self.heart = HEARTH
        self.game_speed = 20
        self.lifes_initial = (self.pos_lifes)
        self.font_lifes= pygame.font.Font(FONT_STYLE, 30)
        self.x_pos_bg = 50
        self.y_pos_bg = 380
        self.obstacle_manager = ObstacleManager()
        self.stats = {
            'deaths': 0,
            'highest_score': 0,
            'current_score': 0,
        }
        self.text_color = BLACK_COLOR = (0,0,0)
        self.lives = 3


    def increment_lives(self):
        self.lives += 1
    def show_lives(self):
        for i in range(self.lives):
            heart_rect = self.heart.get_rect()
            heart_rect.x, heart_rect.y = self.heart_pos[0] + 35 * i, self.heart_pos[1]
            self.screen.blit(self.heart, heart_rect)

    def update_highest_score(self):
        if self.points > self.highest_score:
            self.highest_score = self.points




    def show_score(self):
        self.stats['current_score'] += 1
        if self.stats['current_score'] % 100 == 0 and self.game_speed < 500:
            self.game_speed += 5
        show_score_text =  self.font_lifes.render(f"Points:{self.stats['current_score']}", True, self.text_color)
        self.screen.blit(show_score_text, self.pos_score )
        highest_count_text =  self.font_lifes.render(f"Highest:{self.stats['highest_score']}", True, self.text_color)
        self.screen.blit(highest_count_text,self.pos_highscore)        
        self.show_deaths()
        self.change_color(self.stats['current_score'])



    def change_color(self, score):
        if score % 150 == 0:
            self.color_background,  self.text_color = random.choice([
            ((255, 255, 255), (0,0,0)),
            ((0, 0, 0), (255, 255, 255))
        ])



    def show_deaths(self):
        death_count_text = self.font_lifes.render(f"Deaths: {self.death_count}", True, self.text_color)
        self.screen.blit(death_count_text, self.pos_lifes)



    def show_menu(self):
        # Copiar la superficie en la pantalla
        text,rect = get_center_message("Press any key to start")
        self.screen.blit(text,rect)
        

        self.game_over = GAME_OVER
        self.rect_g = self.game_over.get_rect()
        self.rect_g.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT//3)
        self.screen.blit(self.game_over, self.rect_g)

        text, rect = get_center_message_game(f"Press any key to start")
        self.screen.blit(text, rect)
        self.image = RESET
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2,300)
        self.screen.blit(self.image, self.rect)
        if self.stats['current_score'] > self.stats['highest_score']:
            self.stats['highest_score'] = self.stats['current_score']
        self.stats['current_score'] = 0
        self.stats['deaths'] += 1
        


        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                
                self.playing = False

            if event.type == pygame.KEYDOWN:
                self.lives = 3
                self.color_background = self.WHITE_COLOR
                self.text_color = self.BLACK_COLOR
                self.run() 
                self.stats['deaths'] += 1
                self.death_count += 1
                self.reset()


    def run(self):
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        self.points = 0
        self.obstacle_manager.check_game_status(self)
        self.obstacle_manager.remove_obstacle()
        self.game_speed = GAME_SPEED

    def events(self):
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    def update(self):
        user_input = pygame.key.get_pressed()
        self.cloud.update(self.game_speed)
        self.player.update(user_input)
        self.obstacle_manager.update(self, user_input)
        self.power_up_manager.update(self)



    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill(self.color_background)
        self.show_score()
        self.player.draw(self.screen)
        self.draw_background()
        self.cloud.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.show_lives()

        
        pygame.display.update()
        pygame.display.flip()


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def reset(self):
        self.player.move_to_origin()
        self.power_up_manager.remove_powers()
    
    