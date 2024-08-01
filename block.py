import pygame
import assets
import random
import definitions

#object class
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(assets.block).convert_alpha(), (30,30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velY = random.uniform(3 + definitions.speed_increase,7 + definitions.speed_increase)  # Vertical speed

    def update(self):
        # Move the block down
        self.rect.y += self.velY

def makeBlock():
    block_x = random.randint(0, definitions.screen_width - 20)  # Correctly calculate x position
    block_y = random.randint(-50, -20)  # Starting above the screen
    block = Block(block_x, block_y)
    return block

def bottomScreenBlock(block_group):
    options = [0,1,2]
    weights = [.1,.85,.3]
    block_add = random.choices(options,weights,k=1)
    for block in block_group:
        if block.rect.bottom >= definitions.screen_height - 100:
            block.kill()
            if block_add[0] > 0:
                for num in block_add:
                    block_group.add(makeBlock())


   