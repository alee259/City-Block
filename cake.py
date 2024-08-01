import pygame
import assets
import random
import definitions

#object class
class Cake(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(assets.cake).convert_alpha(), (30,30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velY = random.uniform(3 + definitions.speed_increase,7 + definitions.speed_increase)  # Vertical speed

    def update(self):
        # Move the cake down
        self.rect.y += self.velY

def makeCake():
    cake_x = random.randint(0, definitions.screen_width - 20)  # Correctly calculate x position
    cake_y = random.randint(-50, -20)  # Starting above the screen
    cake = Cake(cake_x, cake_y)
    return cake

def bottomScreenCake(cake_group):
    options = [0,1,2]
    weights = [.15,.85,.1]
    cake_add = random.choices(options,weights,k=1)
    for cake in cake_group:
        if cake.rect.bottom >= definitions.screen_height -100:
            cake.kill()
            if cake_add[0] > 0:
                for num in cake_add:
                    cake_group.add(makeCake())


   