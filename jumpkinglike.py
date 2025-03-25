import pygame

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
screen_width, screen_height = screen.get_size()
Cx, Cy = screen_width / 2, screen_height / 2
keys = pygame.key.get_pressed()


# Farben
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Scoreanzeige
font = pygame.font.Font('freesansbold.ttf', 32)

# Klassen
from Enemy import Enemy
from Player import Player
from Coin import Coin
from Goal import Goal
from Platform import Platform
from Heart import Heart
from Slope import Slope
from Deathzone import Deathzone

def start_game():

    v0x, v0y = 5, 5

    # Globale Variablen für Invincibility und Leben
    INVINCIBLE = False
    HITPOINTS = 3
    score = 0
    HITMOMENT = 0

    # Texture laden und skalieren
    texture_floor = pygame.image.load(r"Texture/Bodentextur.png")
    scaled_texture_floor1 = pygame.transform.scale(texture_floor, (520, 500))

    Plattform_texture = pygame.image.load(r"Texture/FlyingPlattform.png")
    scaled_image_platform = pygame.transform.scale(Plattform_texture, (200, 70))

    texture_Player1 = pygame.image.load(r"Texture\WorrierMain.png")
    scaled_image_Player1 = pygame.transform.scale(texture_Player1, (52, 52))

    texture_moving_enemy = pygame.image.load (r"Texture/MovingEnemy.png")
    scaled_image_enemy1 = pygame.transform.scale(texture_moving_enemy,(75,75))

    texture_Player1_Hit = pygame.image.load(r"Texture\WorrierMainBeschädigt.png")
    scaled_image_Player1_Hit = pygame.transform.scale(texture_Player1_Hit, (52, 52))

    texture_left_wall = pygame.image.load(r"Texture\LinkeWand.png")
    texture_right_wall = pygame.image.load(r"Texture/RechteWand.png")

    texture_left_beam = pygame.image.load(r"Texture\BalkenLinkeWand.png")
    texture_right_beam = pygame.image.load(r"Texture\BalkenRechteWand.png")

    texture_ruby_coin = pygame.image.load (r"Texture\RubyCoin.png")
    scaled_texture_ruby_coin = pygame.transform.scale(texture_ruby_coin, (35, 30))
    texture_gold_coin = pygame.image.load (r"Texture\GoldCoin.png")
    scaled_texture_gold_coin = pygame.transform.scale(texture_gold_coin, (40, 40))

    pygame.mixer.music.load(r"Music\BackgroundMusic1.mp3")
    pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)

    texture_trophy = pygame.image.load(r"Texture\Trophy.png")
    scaled_texture_trophy = pygame.transform.scale(texture_trophy, (70, 70))

    texture_heart = pygame.image.load(r"Texture/Heart.png")
    scaled_texture_heart = pygame.transform.scale(texture_heart, (45, 35))

    bg1 = pygame.image.load (r"Texture\DarkCaveBackground.png")
    bg3 = pygame.image.load(r"Texture\LandscapeBackground.png")
    bg2 = pygame.image.load(r"Texture\MoonBackground.png")

    scaled_bg1 = pygame.transform.scale(bg1, (screen_width, screen_height))
    scaled_bg2 = pygame.transform.scale(bg2, (screen_width, screen_height))
    scaled_bg3 = pygame.transform.scale(bg3, (screen_width, screen_height))

    backgrounds = [scaled_bg1, scaled_bg2, scaled_bg3]

    def draw_background (screen, backgrounds, camera_offset_y, scroll_factor):
        total_height = sum (bg.get_height() for bg in backgrounds)
        offset = (camera_offset_y * scroll_factor) % total_height
        y = -offset
        while y < screen.get_height():
            for bg in backgrounds:
                screen.blit(bg, (0,y))
                y += bg.get_height()
                if y >= screen_height:
                    break

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

    #Liste Rutschen
    list_slope = [
            Slope(RED, 200, 200, 100, "left")
    ]

    list_enemy = [Enemy(BLUE, 200, 100, 75, 75, 4, texture=scaled_image_enemy1)]


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


    #Liste leben
    list_hearts = [Heart(YELLOW, Cx -75, 20, 30, 30, scaled_texture_heart),
                   Heart(YELLOW, Cx -25, 20, 30, 30, scaled_texture_heart),
                   Heart(YELLOW, Cx +25, 20, 30, 30, scaled_texture_heart)]

    # Ziel erstellen
    goal1 = Goal(WHITE, 700, -380, 60, 80,texture=scaled_texture_trophy)

    deathzone1 = Deathzone(WHITE, -1000, 900, 20000, 20000)


    # create player
    player1 = Player(RED, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)

    # Hauptspielschleife
    gameactive = True
    while gameactive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameactive = False

        player1.KeyPress()
        camera_offset_y = player1.y - screen_height / 2
        background_scroll_faktor = 0.2
        draw_background(screen, backgrounds, camera_offset_y, background_scroll_faktor)

        #Gegner zeichen
        for enemy in list_enemy:
            enemy.update()
            enemy.draw(screen, camera_offset_y)

        # Plattformen zeichnen
        for platform in list_platform:
            platform.draw(screen, camera_offset_y)

        #Rutsche zeichnen
        for slope in list_slope:
            slope.draw(screen, camera_offset_y)

        # Coins zeichnen
        for coin in list_ruby_coins:
            coin.draw(screen, camera_offset_y)
        for coin in list_gold_coins:
            coin.draw(screen, camera_offset_y)

        # Goal zeichnen
        goal1.draw(screen, camera_offset_y)

        #Deathzone Zeichnen
        deathzone1.draw(screen, camera_offset_y)
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
                collect = pygame.mixer.Sound(r"Sounds\CoinCollect1.mp3")
                pygame.mixer.Sound.play(collect)
                del list_ruby_coins[i]
                score += 1
        for i in range(len(list_gold_coins)-1, -1, -1):
            if player1.rect.colliderect(list_gold_coins[i].rect):
                collect = pygame.mixer.Sound(r"Sounds\CoinCollect1.mp3")
                pygame.mixer.Sound.play(collect)
                del list_gold_coins[i]
                score += 2

        # Enemy-Kollision
        for enemy in list_enemy:
            if player1.rect.colliderect(enemy.rect):
                if not INVINCIBLE:
                    INVINCIBLE = True
                    HITPOINTS -= 1
                    HITMOMENT = pygame.time.get_ticks()
                    damage = pygame.mixer.Sound(r"Sounds\damage.mp3")
                    pygame.mixer.Sound.play(damage)

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
                victory = pygame.mixer.Sound(r"Sounds\victory1.mp3")
                pygame.mixer.Sound.play(victory)
        else:
            reset_triggered = False

        # Deathzone Kollision
        if player1.rect.colliderect(deathzone1.rect):
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
        score_text = font.render('Score = ' + str(score), True, YELLOW)
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
