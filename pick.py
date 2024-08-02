import pygame
import assets
import random
import definitions

#object class
class Pick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(assets.pick).convert_alpha(), (30,30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velY = random.uniform(3 + definitions.speed_increase,6 + definitions.speed_increase)  # Vertical speed

    def update(self):
        # Move the pick down
        self.rect.y += self.velY

def makePick():
    pick_x = random.randint(definitions.screen_width // 2 - 350, definitions.screen_width // 2  + 350)  # Correctly calculate x position
    pick_y = random.randint(-50, -20)  # Starting above the screen
    pick = Pick(pick_x, pick_y)
    return pick

def bottomScreenPick(pick_group):
    options = [0,1,2]
    weights = [.75,.85,.125]
    pick_add = random.choices(options,weights,k=1)
    for pick in pick_group:
        if pick.rect.bottom >= definitions.screen_height -130:
            pick.kill()
            if pick_add[0] > 0:
                for num in pick_add:
                    pick_group.add(makePick())


   