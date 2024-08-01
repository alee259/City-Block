import pygame
import random
import definitions
import assets
import block
import cake
import bomb
import pick
import sys   

#pygame init
pygame.mixer.pre_init(44100,16,2,4096)
pygame.init()
screen = pygame.display.set_mode((definitions.screen_width, definitions.screen_height))
pygame.display.set_caption(definitions.TITLE)
pygame.display.set_caption('Score:')
pygame.display.set_caption('Lives:')
clock = pygame.time.Clock()
FONT0 = pygame.font.Font(assets.main_font, 36)  # Use default font with size 36
FONT = pygame.font.Font(assets.main_font, 48)  # Use default font with size 36
FONT2 = pygame.font.Font(assets.main_font, 24)
FONT3 = pygame.font.Font(assets.main_font, 70)

#drawing functions
def drawScore(screen, score):
    score_text = f"Score: {score}"
    text_screen = FONT0.render(score_text, True, definitions.WHITE)
    screen.blit(text_screen, (10,960))

def drawLives(screen, lives):
    lives_text = f"Lives: {lives}"
    text_screen = FONT0.render(lives_text, True, definitions.WHITE)
    screen.blit(text_screen, (555,960))

def drawLevel(screen):
    level_text = f"Level: {definitions.speed_increase+1}"
    text = FONT0.render(level_text, True, definitions.WHITE)
    level_rect = text.get_rect(center=(definitions.screen_width // 2,975))
    screen.blit(text, level_rect)

def drawFloor(screen):
    floor_tile = pygame.image.load(assets.floor)
    for num in range(14):
        screen.blit(floor_tile,(num*50,890))


def drawBackground(screen):
    size = pygame.transform.scale(assets.BACKGROND, (800,1200))
    screen.blit(size,(0,0))
    
#screens
def play():

    start_y = definitions.screen_height - 50 - definitions.player_height  # 100 pixels from the bottom
    player_group = pygame.sprite.Group()
    player = definitions.Player(definitions.screen_width // 2 - definitions.player_width // 2, start_y)  # Center horizontally
    player_group.add(player)
    pygame.mixer.music.load(assets.game_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    prev_score = player.score

    #object setup
    block_group = pygame.sprite.Group()
    numBlock = random.randint(9, 13)
    for _ in range(numBlock):
        block_group.add(block.makeBlock())

    cake_group = pygame.sprite.Group()
    numCake = random.randint(1, 3)
    for _ in range(numCake):
        cake_group.add(cake.makeCake())

    bomb_group = pygame.sprite.Group()
    numBomb = random.randint(6+definitions.bomb_increase,8+definitions.bomb_increase)
    for _ in range(numBomb):
        bomb_group.add(bomb.makeBomb())

    pick_group = pygame.sprite.Group()
    numPick = random.randint(2,4)
    for _ in range(numPick):
        pick_group.add(pick.makePick())    

    run = True

    while run:

        #drawing objects
        screen.fill("black")
        drawBackground(screen)
        player_group.draw(screen)
        drawScore(screen,player.score)
        drawLives(screen,player.lives)
        drawLevel(screen)
        drawFloor(screen)
        block_group.draw(screen)
        cake_group.draw(screen)
        bomb_group.draw(screen)
        pick_group.draw(screen)

        #check level
        if player.score - prev_score == definitions.SCORE_INCREMENT:
            definitions.speed_increase += 1
            definitions.bomb_increase += 1
            prev_score = player.score

        #Block Logic
        for obj in block_group:
            if pygame.sprite.spritecollide(obj, player_group, False, pygame.sprite.collide_mask):
                obj.kill()
                block_group.add(block.makeBlock())
                player.score += 1
        if len(block_group) < 8:
            for num in range(8-len(block_group)):
                block_group.add(block.makeBlock())

        #Cake Logic
        for obj in cake_group:
            if pygame.sprite.spritecollide(obj, player_group, False, pygame.sprite.collide_mask):
                obj.kill()
                cake_group.add(cake.makeCake())
                if player.lives < 3:    
                    player.lives += 1
        if len(cake_group) < 2:
            for num in range(2-len(cake_group)):
                cake_group.add(cake.makeCake())

        #Bomb Logic
        for obj in bomb_group:
            if pygame.sprite.spritecollide(obj, player_group, False, pygame.sprite.collide_mask):
                obj.kill()
                bomb_group.add(bomb.makeBomb())
                player.lives -= 1
        if len(bomb_group) < 7:
            for num in range(7-len(bomb_group)):
                bomb_group.add(bomb.makeBomb()) 

        #Pick Logic
        for obj in pick_group:
            if pygame.sprite.spritecollide(obj, player_group, False, pygame.sprite.collide_mask):
                obj.kill()
                pick_group.add(pick.makePick()) 
                player.score += 2
        if len(pick_group) < 2:
            for num in range(2-len(pick_group)):
                pick_group.add(pick.makePick())

        #checking lives
        if player.lives == 0:
            death()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.left_pressed = True
                    player.animate(1)
                if event.key == pygame.K_d:
                    player.right_pressed = True
                    player.animate(1)
                if event.key == pygame.K_ESCAPE:
                    pause()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.left_pressed = False
                    player.animate(0)
                if event.key == pygame.K_d:
                    player.right_pressed = False
                    player.animate(0)

        #update
        player_group.update()
        block_group.update()
        cake_group.update()
        bomb_group.update()
        pick_group.update()
        block.bottomScreenBlock(block_group)
        cake.bottomScreenCake(cake_group)
        bomb.bottomScreenBomb(bomb_group)
        pick.bottomScreenPick(pick_group)
        pygame.display.flip()
        clock.tick(120)

def instructions():
    pygame.display.set_caption(definitions.TITLE)
    pygame.mixer.music.load(assets.main_menu_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while True:
        screen.fill("black")
        MOUSE_POS = pygame.mouse.get_pos()
        INSTRUCTIONS = FONT.render("Instructions", True, "white")
        MENU_RECT = INSTRUCTIONS.get_rect(center=(definitions.screen_width // 2,150))
        main_text1 = FONT2.render("The city has been destroyed!", True, "white")
        main_text2 = FONT2.render("Catch items to rebuild it, but avoid bombs!", True, "white")
        main_text3 = FONT2.render("Avoid the bombs, they will decrease your lives!", True, "white")
        main_text4 = FONT2.render("Pickaxes are two points, blocks are one!", True, "white")
        main_text5 = FONT2.render("Cake slices are one bonus life (Max of 3)!", True, "white")
        main_text6 = FONT2.render("You can move left and right with A and D keys.", True, "white") 
        main_text7 = FONT2.render("Use ESC to pause!", True, "white")
        main_text8 = FONT2.render("Every 100 score points, the game speeds up", True, "white")
        main_text9 = FONT2.render("and more bombs will spawn!", True, "white")

        main_text1_rect = main_text1.get_rect(center=(definitions.screen_width // 2, 300))
        main_text2_rect = main_text2.get_rect(center=(definitions.screen_width // 2, 350))
        main_text3_rect = main_text3.get_rect(center=(definitions.screen_width // 2, 400))
        main_text4_rect = main_text4.get_rect(center=(definitions.screen_width // 2, 450))
        main_text5_rect = main_text5.get_rect(center=(definitions.screen_width // 2, 500))
        main_text6_rect = main_text6.get_rect(center=(definitions.screen_width // 2, 550))
        main_text7_rect = main_text7.get_rect(center=(definitions.screen_width // 2, 600))
        main_text8_rect = main_text8.get_rect(center=(definitions.screen_width // 2, 650))
        main_text9_rect = main_text9.get_rect(center=(definitions.screen_width // 2, 700))

        PLAY_BUTTON = definitions.Button(None, pos=(75,960),text_input = "PLAY", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        QUIT = definitions.Button(None, pos=(625,960),text_input = "QUIT", font=FONT, base_color = "#d7fcd4", hovering_color = "white")

        screen.blit(INSTRUCTIONS, MENU_RECT)
        screen.blit(main_text1, main_text1_rect)
        screen.blit(main_text2, main_text2_rect)
        screen.blit(main_text3, main_text3_rect)
        screen.blit(main_text4, main_text4_rect)
        screen.blit(main_text5, main_text5_rect)
        screen.blit(main_text6, main_text6_rect)
        screen.blit(main_text7, main_text7_rect)
        screen.blit(main_text8, main_text8_rect)
        screen.blit(main_text9, main_text9_rect)

        buttons = [PLAY_BUTTON, QUIT]
        for button in buttons:
            button.colorChange(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].input(MOUSE_POS):
                    play()
                if buttons[1].input(MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(120)

def death():
    pygame.display.set_caption(definitions.TITLE)
    pygame.mixer.music.load(assets.death_sound)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(1)

    while True:
        screen.fill("black")
        MOUSE_POS = pygame.mouse.get_pos()
        DEATH_TEXT = FONT.render("You died!", True, "white")
        MENU_RECT = DEATH_TEXT.get_rect(center=(definitions.screen_width // 2,250))

        QUIT = definitions.Button(None, pos=(definitions.screen_width // 2,550),text_input = "QUIT", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        PLAY_AGAIN = definitions.Button(None, pos=(definitions.screen_width // 2,450),text_input = "PLAY AGAIN?", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        MAIN_MENU = definitions.Button(None, pos=(definitions.screen_width // 2,650),text_input = "MAIN MENU", font=FONT, base_color = "#d7fcd4", hovering_color = "white")

        screen.blit(DEATH_TEXT, MENU_RECT)

        buttons = [PLAY_AGAIN, QUIT,MAIN_MENU]
        for button in buttons:
            button.colorChange(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].input(MOUSE_POS):
                    play()
                if buttons[1].input(MOUSE_POS):
                    pygame.quit()
                    sys.exit()
                if buttons[2].input(MOUSE_POS):
                    main_menu()
        
        pygame.display.flip()
        clock.tick(120)

def main_menu():
    pygame.display.set_caption(definitions.TITLE)
    pygame.mixer.music.load(assets.main_menu_music)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
                            

    while True:
        screen.fill("black")
        MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = FONT.render("Main Menu", True, "white")
        MENU_RECT = MENU_TEXT.get_rect(center=(definitions.screen_width // 2,230))
        TITLE_TEXT = FONT3.render("City Block", True, "white")
        TITLE_RECT = TITLE_TEXT.get_rect(center=(definitions.screen_width // 2,110))
        PLAY_BUTTON = definitions.Button(None, pos=(definitions.screen_width // 2,450),text_input = "PLAY", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        INSTRUCTIONS = definitions.Button(None, pos=(definitions.screen_width // 2,600),text_input = "INSTRUCTIONS", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        QUIT = definitions.Button(None, pos=(definitions.screen_width // 2,750),text_input = "QUIT", font=FONT, base_color = "#d7fcd4", hovering_color = "white")

        screen.blit(MENU_TEXT,MENU_RECT)
        screen.blit(TITLE_TEXT,TITLE_RECT)


        buttons = [PLAY_BUTTON, INSTRUCTIONS, QUIT]
        for button in buttons:
            button.colorChange(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].input(MOUSE_POS):
                    play()
                if buttons[1].input(MOUSE_POS):
                    instructions()
                if buttons[2].input(MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()
        clock.tick(120)

def pause():
    pause = True

    while pause:
        screen.fill("black")
        MOUSE_POS = pygame.mouse.get_pos()
        QUIT = definitions.Button(None, pos=(definitions.screen_width // 2,400),text_input = "QUIT", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        RESUME = definitions.Button(None, pos=(definitions.screen_width // 2,550),text_input = "RESUME", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        MAIN_MENU = definitions.Button(None, pos=(definitions.screen_width // 2,700),text_input = "MAIN MENU", font=FONT, base_color = "#d7fcd4", hovering_color = "white")
        PAUSE = FONT.render("PAUSE", True, "white")
        PAUSE_RECT = PAUSE.get_rect(center=(definitions.screen_width // 2,200))
        buttons = [QUIT,RESUME,MAIN_MENU]

        screen.blit(PAUSE, PAUSE_RECT)

        for button in buttons:
            button.colorChange(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttons[0].input(MOUSE_POS):
                   pygame.quit()
                   sys.exit()
                if buttons[1].input(MOUSE_POS):
                    pause = False
                if buttons[2].input(MOUSE_POS):
                    main_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause = False
        
        pygame.display.flip()
        clock.tick(120)
                    

#start game
main_menu()