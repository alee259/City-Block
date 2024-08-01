import pygame
import assets
import random

#var init
TITLE = 'City Block'
OBJ_SIZE = 20
player_height = 160
player_width = 116
screen_width = 700
screen_height = 1000
speed_increase = 0
SCORE_INCREMENT = 100
bomb_increase = 0

#colors
RED  = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
BG = (50,50,50)
ORANGE = (250,120,60)
WHITE = (255,255,255)
PINK = (255,192,203)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.run_right = []
        self.idle_right = []
        for i in range(6):
            self.run_right.append(pygame.image.load(getattr(assets, f'mechanicr{i}')).convert_alpha())
        for i in range(2):
            self.idle_right.append(pygame.image.load(getattr(assets, f'mechanici{i}')).convert_alpha())
        self.run_left = [pygame.transform.flip(img, True, False) for img in self.run_right]
        self.idle_left = [pygame.transform.flip(img, True, False) for img in self.idle_right]
        self.current_run = 0
        self.current_idle = 0
        self.running = False
        self.image = self.idle_right[self.current_idle]
        self.facing_right = True
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = x
        self.y = y
        self.left_pressed = False
        self.right_pressed = False
        self.speed = 3.5
        self.score = 0
        self.lives = 3

    def update(self):
        self.velX = 0
        if self.left_pressed and not self.right_pressed:
            self.velX = -self.speed
            self.facing_right = False
        if self.right_pressed and not self.left_pressed:
            self.velX = self.speed
            self.facing_right = True

        self.rect.x += self.velX

        if self.rect.left < 0-40:
            self.rect.left = 0-40
        if self.rect.right > screen_width+40:
            self.rect.right = screen_width+40


        if self.running == True:
            self.current_run += .065
            if self.current_run >= len(self.run_right):
                self.current_run = 0
            if self.facing_right == True:
                self.image = self.run_right[int(self.current_run)]
            else:
                self.image = self.run_left[int(self.current_run)]
        elif self.running == False:
            self.current_idle += .035
            if self.current_idle >= len(self.idle_right):
                self.current_idle = 0
            if self.facing_right == True:
                self.image = self.idle_right[int(self.current_idle)]
            else:
                self.image = self.idle_left[int(self.current_idle)]


    def animate(self, int):
        if int == 1:
            self.running = True
        elif int == 0:
            self.running = False
 

#button
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input,True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x,self.y))
    
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    
    def input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            return True 
        return False
    
    def colorChange(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,self.rect.bottom):
            self.text = self.font.render(self.text_input,True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input,True, self.base_color)

