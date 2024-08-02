import pygame
import assets
import random
import definitions

#object class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(assets.bomb).convert_alpha(), (30,30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velY = random.uniform(3 + definitions.speed_increase,7 + definitions.speed_increase)  # Vertical speed

    def update(self):
        # Move the bomb down
        self.rect.y += self.velY

def makeBomb():
    bomb_x = random.randint(definitions.screen_width // 2 - 350, definitions.screen_width // 2  + 350)  # Correctly calculate x position
    bomb_y = random.randint(-50, -20)  # Starting above the screen
    bomb = Bomb(bomb_x, bomb_y)
    return bomb

def bottomScreenBomb(bomb_group):
    options = [0,1,2]
    weights = [.75,.85,.3]
    bomb_add = random.choices(options,weights,k=1)
    for bomb in bomb_group:
        if bomb.rect.bottom >= definitions.screen_height -130:
            bomb.kill()
            if bomb_add[0] > 0:
                for num in bomb_add:
                    bomb_group.add(makeBomb())


   