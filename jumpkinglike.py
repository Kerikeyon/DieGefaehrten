import pygame

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
screen_width, screen_height = screen.get_size()
Cx, Cy = screen_width / 2, screen_height / 2
v0x, v0y = 5, 5

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
ORANGE = (255, 128, 0)
GELB = (255, 255, 0)
GRÜN = (0, 255, 0)
BLAU = (0, 0, 255)

# Globale Variablen für Invincibility und Leben
INVINCIBLE = False
LEBEN = 3
score = 0
HITMOMENT = 0

# Scoreanzeige
font = pygame.font.Font('freesansbold.ttf', 32)

# Klassen
from Gegner import Gegner
from Player import Player
from Coin import Coin
from Goal import Goal
from Platform import Platform
from Heart import Heart

# Texturen laden und skalieren
texture_Boden = pygame.image.load(r"Texturen\Bodentextur2.webp")
scaled_texture_floor1 = pygame.transform.scale(texture_Boden, (520, 500))

Plattform_texture = pygame.image.load(r"Texturen\Flying_Plattform.png")
scaled_image_platform = pygame.transform.scale(Plattform_texture, (200, 70))

texture_Player1 = pygame.image.load(r"Texturen\WorrierMain.png")
scaled_image_Player1 = pygame.transform.scale(texture_Player1, (52, 52))

texture_left_wall = pygame.image.load(r"Texturen\Linke Wand.png")
texture_right_wall = pygame.image.load(r"Texturen\Rechte Wand.png")

texture_left_beam = pygame.image.load(r"Texturen\BalkenLinkeWand.png")
texture_right_beam = pygame.image.load(r"Texturen\BalkenRechteWand.png")

texture_ruby_coin = pygame.image.load (r"Texturen\RubyCoin.png")
scaled_texture_ruby_coin = pygame.transform.scale(texture_ruby_coin, (35, 30))
texture_gold_coin = pygame.image.load (r"Texturen\GoldCoin.jpeg")
scaled_texture_gold_coin = pygame.transform.scale(texture_gold_coin, (40, 40))


#Liste Plattformen
list_platform = [
    Platform(SCHWARZ, -20, 570, 520, 500, texture=scaled_texture_floor1),
    Platform(SCHWARZ, 500, 570, 520, 500, texture=scaled_texture_floor1),
    Platform(WEISS, 640, 400, 200, 30, texture=scaled_image_platform),
    Platform(WEISS, 440, 10, 200, 30, texture=scaled_image_platform),
    Platform(WEISS, 70, -200, 200, 30, texture=scaled_image_platform),
    Platform(WEISS, 13, 203, 451, 47, texture=texture_left_beam),
    Platform(WEISS, 538, -309, 451, 47, texture=texture_right_beam),
    Platform(SCHWARZ, 0, -30, 40, 700, texture=texture_left_wall),
    Platform(SCHWARZ, 0, -630, 40, 700, texture=texture_left_wall),
    Platform(SCHWARZ, 1000-53, -30, 40, 700, texture=texture_right_wall),
    Platform(SCHWARZ, 1000-53, -630, 40, 700, texture=texture_right_wall),
]

list_gegner = [Gegner(BLAU, 100, 100, 75, 75, 4)]


#Origin Liste Coins
origin_ruby_coins = [
    (ROT, 525, -30, 30, 30, scaled_texture_ruby_coin),
]

origin_gold_coins = [
    (GELB, 300, 160, 30, 30, scaled_texture_gold_coin)
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
list_hearts = [Heart(ROT, 20, 20, 40, 40, None), Heart(ROT, 80, 20, 40, 40, None), Heart(ROT, 140, 20, 40, 40, None)]

# Ziel erstellen
goal1 = Goal(GRÜN, 700, -400, 50, 50)

#Gegner erstellen
#Gegner(BLAU, 100, 100, 75, 75, 4)

# Spieler erstellen
player1 = Player(ROT, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)

# Hauptspielschleife
spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False




    player1.KeyPress()
    camera_offset_y = player1.y - screen_height / 2
    screen.fill(WEISS)



    for gegner in list_gegner:
        gegner.update()
        gegner.draw(screen, camera_offset_y)
        #pygame.draw.rect(screen, gegner.f, gegner1.rect)


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
    for platform in list_platform:
        if player1.rect.colliderect(platform.rect):
            player1.v[1] = 0
            # Kollision von oben
            if (player1.rect.y + player1.rect.h) > platform.rect.y > player1.rect.y:
                player1.y = platform.rect.y - player1.rect.h + 0.5
                player1.isOnPlatform = 0
            # Kollision von unten
            elif player1.rect.y < (platform.rect.y + platform.rect.h) < (player1.rect.y + player1.rect.h):
                player1.y = platform.rect.y + platform.rect.h
            # Kollision von links
            elif (player1.rect.x + player1.rect.w) > platform.rect.x > player1.rect.x:
                player1.v[0] = 0
                player1.x = platform.rect.x - player1.rect.w
            # Kollision von rechts
            elif player1.rect.x < (platform.rect.x + platform.rect.w) < (player1.rect.x + player1.rect.w):
                player1.v[0] = 0
                player1.x = platform.rect.x + platform.rect.w
            player1.v[0] = v0x

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
    for gegner in list_gegner:
        if player1.rect.colliderect(gegner.rect):
            if not INVINCIBLE:
                INVINCIBLE = True
                LEBEN -= 1
                HITMOMENT = pygame.time.get_ticks()

    if INVINCIBLE:
        player1.f = ORANGE
        current_time = pygame.time.get_ticks()
        if current_time - HITMOMENT >= 1000:
            INVINCIBLE = False
            player1.f = ROT

    # Goal Kollision
    reset_triggered = False
    if player1.rect.colliderect(goal1.rect):
        if not reset_triggered:
            reset_triggered = True  # Reset nur einmal auslösen
            player1 = Player(ROT, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)
            list_ruby_coins[:] = create_ruby_coins()
            list_gold_coins[:] = create_gold_coins()
            score = 0
            INVINCIBLE = False
            LEBEN = 3
    else:
        reset_triggered = False

    # Spieler-Reset
    if LEBEN <= 0:
        LEBEN = 3
        score = 0
        list_ruby_coins[:] = create_ruby_coins()
        list_gold_coins[:] = create_gold_coins()
        player1 = Player(ROT, Cx - 25, 450, 50, 50, texture=scaled_image_Player1)

    # Scoreanzeige zeichnen
    score_text = font.render('Score = ' + str(score), True, GRÜN)
    screen.blit(score_text, (750, 50))

    for i in range(LEBEN):
        list_hearts[i].draw(screen, 0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()