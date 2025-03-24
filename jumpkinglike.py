import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()
Cx, Cy = screen_width / 2, screen_height / 2#hi
keys = pygame.key.get_pressed()

# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)#blabla

# Scoreanzeige
font = pygame.font.Font('freesansbold.ttf', 32)

# Klassen
from Enemy import Enemy
from Player import Player
from Coin import Coin
from Goal import Goal
from Platform import Platform
from Heart import Heart

def start_game():

    v0x, v0y = 5, 5
    

    # Globale Variablen für Invincibility und Leben
    INVINCIBLE = False
    HITPOINTS = 3
    score = 0
    HITMOMENT = 0

    # Texturen laden und skalieren
    texture_floor = pygame.image.load(r"Texturen\Bodentextur2.webp")
    scaled_texture_floor1 = pygame.transform.scale(texture_floor, (520, 500))

    Plattform_texture = pygame.image.load(r"Texturen\Flying_Plattform.png")
    scaled_image_platform = pygame.transform.scale(Plattform_texture, (200, 70))

    texture_Player1 = pygame.image.load(r"Texturen\WorrierMain.png")
    scaled_image_Player1 = pygame.transform.scale(texture_Player1, (52, 52))

    texture_Player1_Hit = pygame.image.load(r"Texturen\WorrierMainBeschädigt.png")
    scaled_image_Player1_Hit = pygame.transform.scale(texture_Player1_Hit, (52, 52))

    texture_left_wall = pygame.image.load(r"Texturen\Linke Wand.png")
    texture_right_wall = pygame.image.load(r"Texturen\Rechte Wand.png")

    texture_left_beam = pygame.image.load(r"Texturen\BalkenLinkeWand.png")
    texture_right_beam = pygame.image.load(r"Texturen\BalkenRechteWand.png")

    texture_ruby_coin = pygame.image.load (r"Texturen\RubyCoin.png")
    scaled_texture_ruby_coin = pygame.transform.scale(texture_ruby_coin, (35, 30))
    texture_gold_coin = pygame.image.load (r"Texturen\GoldCoin.jpeg")
    scaled_texture_gold_coin = pygame.transform.scale(texture_gold_coin, (40, 40))

    #hallo
    #Liste Plattformen
    list_platform = [
        Platform(BLACK, -20, 570, 520, 500, texture=scaled_texture_floor1),
        Platform(BLACK, 500, 570, 520, 500, texture=scaled_texture_floor1),
        Platform(WHITE, 640, 400, 200, 30, texture=scaled_image_platform),
        Platform(WHITE, 440, 10, 200, 30, texture=scaled_image_platform),
        Platform(WHITE, 70, -200, 200, 30, texture=scaled_image_platform),
        Platform(WHITE, 13, 203, 451, 47, texture=texture_left_beam),
        Platform(WHITE, 538, -309, 451, 47, texture=texture_right_beam),
        Platform(BLACK, 0, -30, 40, 700, texture=texture_left_wall),
        Platform(BLACK, 0, -630, 40, 700, texture=texture_left_wall),
        Platform(BLACK, 1000-53, -30, 40, 700, texture=texture_right_wall),
        Platform(BLACK, 1000-53, -630, 40, 700, texture=texture_right_wall),
    ]

    list_enemy = [Enemy(BLUE, 100, 100, 75, 75, 4)]


    #Origin Liste Coins
    origin_ruby_coins = [
        (RED, 525, -30, 30, 30, scaled_texture_ruby_coin),
    ]

    origin_gold_coins = [
        (YELLOW, 300, 160, 30, 30, scaled_texture_gold_coin)
    ]

    def create_ruby_coins():
        return [Coin(color, x, y, width, height, texture=texture)
                for color, x, y, width, height, texture in origin_ruby_coins]
    def create_gold_coins():
        return [Coin(color, x, y, width, height, texture=texture)
                for color, x, y, width, height, texture in origin_gold_coins]

    list_ruby_coins = create_ruby_coins()
    list_gold_coins = create_gold_coins()

    #List leben
    list_hearts = [Heart(RED, 20, 20, 40, 40, None), Heart(RED, 80, 20, 40, 40, None), Heart(RED, 140, 20, 40, 40, None)]

    # create goal
    goal1 = Goal(GREEN, 700, -400, 50, 50)

    # create player
    player1 = Player(RED, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)

    # main game loop
    gameactive = True

    while gameactive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameactive = False
        
        player1.KeyPress()
        camera_offset_y = player1.y - screen_height / 2
        screen.fill(WHITE)


        #Gegner zeichen
        for enemy in list_enemy:
            enemy.update()
            enemy.draw(screen, camera_offset_y)
                
        # Plattformen zeichnen
        for platform in list_platform:
            platform.draw(screen, camera_offset_y)
        # Coins zeichnen
        for coin in list_ruby_coins:
            coin.draw(screen, camera_offset_y)
        for coin in list_gold_coins:
            coin.draw(screen, camera_offset_y)

        # Goal zeichnen
        goal1.draw(screen, camera_offset_y)

        # Spieler zeichnen
        player1.draw(screen, camera_offset_y)

        # Physik
        player1.applyGravity()
        player1.jump()
        # Plattform-Kollisionen
        player1.handle_collisions(list_platform)
        player1.rect.topleft = (player1.x, player1.y)
        player1.resetJump()

        # Coin-Kollision
        for i in range(len(list_ruby_coins)-1, -1, -1):
            if player1.rect.colliderect(list_ruby_coins[i].rect):
                del list_ruby_coins[i]
                score += 1
        for i in range(len(list_gold_coins)-1, -1, -1):
            if player1.rect.colliderect(list_gold_coins[i].rect):
                del list_gold_coins[i]
                score += 2

        # Enemy-Kollision
        for enemy in list_enemy:
            if player1.rect.colliderect(enemy.rect):
                if not INVINCIBLE:
                    INVINCIBLE = True
                    HITPOINTS -= 1
                    HITMOMENT = pygame.time.get_ticks()
        if INVINCIBLE:
            player1.texture = scaled_image_Player1_Hit
            player1.f = ORANGE
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - HITMOMENT
            
            if (elapsed_time // 50) % 2 == 0:
                player1.texture = scaled_image_Player1_Hit
            else:
                player1.texture = scaled_image_Player1
            if current_time - HITMOMENT >= 1000:
                player1.texture = scaled_image_Player1
                INVINCIBLE = False
                player1.f = RED
                player1.texture = scaled_image_Player1

        # Goal Kollision
        reset_triggered = False
        if player1.rect.colliderect(goal1.rect):
            if not reset_triggered:
                reset_triggered = True  # Reset nur einmal auslösen
                player1 = Player(RED, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)
                list_ruby_coins[:] = create_ruby_coins()
                list_gold_coins[:] = create_gold_coins()
                score = 0
                INVINCIBLE = False
                HITPOINTS = 3
        else:
            reset_triggered = False

        # Spieler-Reset
        if HITPOINTS <= 0:
            HITPOINTS = 3
            score = 0
            list_ruby_coins[:] = create_ruby_coins()
            list_gold_coins[:] = create_gold_coins()
            player1 = Player(RED, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)

        # Scoreanzeige zeichnen
        score_text = font.render('Score = ' + str(score), True, BLACK)
        screen.blit(score_text, (37, 65))


        for i in range(HITPOINTS):
            list_hearts[i].draw(screen, 0)
        
        #menu button
        button(900, 50, 40, 40, '...', 0, 0, (210,210,210))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# values after 'text' are for centralizing text
def button(x, y, w, h, text, text_offset_x, text_offset_y, color):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = font.render((text), True, BLACK)
    screen.blit(button_text, (x + text_offset_x, y + text_offset_y))

    if mouse_pos[0] >= x and mouse_pos[0] <= x + w and mouse_pos[1] >= y and mouse_pos[1] <= y + h:
        pygame.draw.rect(screen, (210, 210, 210), (x, y, w, h))
        screen.blit(button_text, (x + text_offset_x, y + text_offset_y))
        if click[0]:
            if text == 'Start':
                start_game()
            elif text == 'Options':
                options()
            elif text == 'Quit':
                pygame.quit()
            elif text == 'Back':
                menu()
            elif text == '...':
                menu()

def menu():
 
 while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
    pygame.display.update()

    screen.fill(BLACK)
    button(Cx - 100, 100, 200, 70, 'Start', 50, 20, WHITE)
    button(Cx - 100, 225, 200, 70, 'Options', 40, 20, WHITE)
    button(Cx - 100, 350, 200, 70, 'Quit', 50, 20, WHITE)
 
def options():
 while True:

    for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
    pygame.display.update()
    screen.fill(BLACK)
    button(Cx - 100, 100, 200, 70, 'Test 1', 37, 20, WHITE)
    button(Cx - 100, 225, 200, 70, 'Test 2', 60, 20, WHITE)
    button(Cx - 100, 350, 200, 70, 'Test 3', 40, 20, WHITE)
    button(Cx - 100, 475, 200, 70, 'Back', 40, 20, WHITE)

menu()