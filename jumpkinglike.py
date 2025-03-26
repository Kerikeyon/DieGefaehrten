import pygame

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
game_running = False
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
from Enemy_Horizontal import Enemy_Horizontal
from Enemy_Vertical import Enemy_Vertical
from Player import Player
from Coin import Coin
from Goal import Goal
from Platform import Platform
from Heart import Heart
from Slope import Slope
from Deathzone import Deathzone
from PowerUp import PowerUp
from Static_Enemy import Static_Enemy

def start_game():

    v0x, v0y = 5, 5
    

    # Globale Variablen für Invincibility und Leben
    invincible = False
    hitpoints = 3
    score = 0
    hitmoment = 0

    # Texture laden und skalieren
    texture_floor = pygame.image.load(r"Texture/Bodentextur.png")
    scaled_texture_floor1 = pygame.transform.scale(texture_floor, (520, 500))

    texture_flying_plattform = pygame.image.load(r"Texture/FlyingPlattform.png")
    scaled_image_platform = pygame.transform.scale(texture_flying_plattform, (200, 70))
    scaled_image_platform2 = pygame.transform.scale(texture_flying_plattform, (100,35))

    texture_slippery_middle = pygame.image.load(r"Texture/SlipperyMitte.png")
    scaled_slippery_middle = pygame.transform.scale(texture_slippery_middle, (50, 88))
    texture_slippery_left = pygame.image.load(r"Texture/SlipperyLinks.png")
    scaled_slippery_left = pygame.transform.scale(texture_slippery_left, (55, 55))
    texture_slippery_right = pygame.image.load(r"Texture/SlipperyRechts.png")
    scaled_slippery_right = pygame.transform.scale(texture_slippery_right, (55, 55))

    texture_player1 = pygame.image.load(r"Texture\WorrierMain.png")
    scaled_image_player1 = pygame.transform.scale(texture_player1, (52, 52))

    texture_moving_enemy = pygame.image.load (r"Texture/MovingEnemy.png")
    scaled_image_enemy1 = pygame.transform.scale(texture_moving_enemy,(75,75))
    texture_spikes = pygame.image.load(r"Texture/Spikes.png")
    scaled_spikes = pygame.transform.scale(texture_spikes, (200,50))
    texture_short_spikes =pygame.image.load(r"Texture/ShortSpikes.png")
    scaled_short_spikes = pygame.transform.scale(texture_short_spikes, (100,50))

    texture_player1_hit = pygame.image.load(r"Texture\WorrierMainBeschädigt.png")
    scaled_image_player1_hit = pygame.transform.scale(texture_player1_hit, (52, 52))

    texture_left_beam = pygame.image.load(r"Texture\BalkenLinkeWand.png")
    scaled_left_beam = pygame.transform.scale(texture_left_beam, (475, 47))
    texture_right_beam = pygame.image.load(r"Texture\BalkenRechteWand.png")

    texture_left_wall = pygame.image.load(r"Texture\LinkeWand.png")
    texture_right_wall = pygame.image.load(r"Texture/RechteWand.png")

    texture_stone_pole_short = pygame.image.load(r"Texture/StonePoleShort.png")

    texture_slope_right = pygame.image.load(r"Texture/RutscheRechts.png")
    scaled_slope_right = pygame.transform.scale(texture_slope_right, (50, 50))
    texture_slope_left = pygame.image.load(r"Texture/RutscheLinks.png")
    scaled_slope_left = pygame.transform.scale(texture_slope_left, (50, 50))

    texture_right_short_straight_beam = pygame.image.load(r"Texture/BalkenGeradeRechts.png")
    scaled_right_straight_short = pygame.transform.scale(texture_right_short_straight_beam, (120, 50))

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

    texture_double_jump = pygame.image.load(r"Texture/DoubleJumpIcon.png")
    scaled_double_jump_icon = pygame.transform.scale(texture_double_jump, (50, 50))

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
    Platform(WHITE, -20, 570, 520, 500, texture=scaled_texture_floor1),
    Platform(WHITE, 500, 570, 520, 500, texture=scaled_texture_floor1),

    Platform(WHITE, 640, 400, 200, 30, texture=scaled_image_platform),
    Platform(WHITE, 640, 10, 200, 30, texture=scaled_image_platform),
    Platform(WHITE, 100, -100, 200, 30, texture=scaled_image_platform),
    Platform(WHITE, 100, -1000, 200, 30, texture=scaled_image_platform),
    Platform(WHITE, 250, -1600, 200, 30, texture=scaled_image_platform),
    Platform(WHITE, 60, -570, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 550, -1770, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 750, -1970, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 500, -2170, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 270, -2170, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 70, -2170, 100, 15, texture=scaled_image_platform2),
    Platform(WHITE, 300, -2570, 100, 15, texture=scaled_image_platform2),

    Platform(WHITE, 16, 203, 451, 47, texture=texture_left_beam),
    Platform(WHITE, 560, -309, 451, 47, texture=texture_right_beam),
    Platform(WHITE, 13,-396,460, 47, texture=scaled_left_beam),
    Platform(WHITE,13,-2000,451,47,texture=texture_left_beam),
    Platform(WHITE,323,-767,120,50,texture=scaled_right_straight_short),

    Platform(WHITE, 0, -30, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -630, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -1230, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 1000-53, -30, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000-53, -630, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000-53, -1230, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 0, -30, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -630, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -1230, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -1830, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 0, -2430, 40, 700, texture=texture_left_wall),
    Platform(WHITE, 1000-53, -30, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000-53, -630, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000-53, -1230, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000 - 53, -1830, 40, 700, texture=texture_right_wall),
    Platform(WHITE, 1000 - 53, -2430, 40, 700, texture=texture_right_wall),

    Platform(WHITE,-10,-4000,10,3000, texture=None),
    Platform(WHITE,1000, -4000, 10, 3000, texture=None),

    Platform(WHITE,425 ,-717,50,324, texture=texture_stone_pole_short),
    Platform(WHITE,650,-2600,50,50,texture=scaled_slippery_middle)
    #Slippery1
    #Platform(WHITE,650,-2600,50,50,texture=scaled_slippery_middle),
    #Platform(BLACK,595,-2544,160,2)
    ]

    #Liste Rutsche
    list_slopes = [
        Slope(RED, 442, -767, 60, "right", texture=scaled_slope_right),
        #Slippery1
        #Slope(RED, 595,-2599,55,"left",texture=scaled_slippery_left),
        #Slope (RED, 700, -2599, 55,"right",texture=scaled_slippery_right),
    ]
    #Liste Gegner
    list_enemy = \
        [Enemy_Horizontal(BLUE, 200, 100, 75, 75, 4,movrange=150, texture=scaled_image_enemy1),
        Enemy_Horizontal(BLUE, 700, -700,75,75,4,movrange=180, texture=scaled_image_enemy1),
        Enemy_Vertical(BLUE, 300, -2250,75,75,5,movrange=250,texture=scaled_image_enemy1),
                  ]

    list_static_enemy = \
        [Static_Enemy(BLUE, 60, -445, 200, 50, texture=scaled_spikes),
         Static_Enemy(BLUE, 500, 530, 100, 50, texture=scaled_short_spikes),

                      ]
    #Liste Coins
    origin_ruby_coins = [
        (RED, 723, -29, 30, 30, scaled_texture_ruby_coin),
        (RED,183, -136,30,30 ,scaled_texture_ruby_coin),
    ]
    origin_gold_coins = [
        (YELLOW, 370, -445, 30, 30, scaled_texture_gold_coin)
    ]
    #coin erstellen r
    def create_ruby_coins():
        return [Coin(color, x, y, width, height, texture=texture)
                for color, x, y, width, height, texture in origin_ruby_coins]
    def create_gold_coins():
        return [Coin(color, x, y, width, height, texture=texture)
                for color, x, y, width, height, texture in origin_gold_coins]
    list_ruby_coins = create_ruby_coins()
    list_gold_coins = create_gold_coins()

    #Liste Leben
    list_hearts = [Heart(YELLOW, Cx -75, 20, 30, 30, scaled_texture_heart),
                   Heart(YELLOW, Cx -25, 20, 30, 30, scaled_texture_heart),
                   Heart(YELLOW, Cx +25, 20, 30, 30, scaled_texture_heart)]

    list_powerups = [PowerUp(410, -200, 40, 40, texture=scaled_double_jump_icon),
                     PowerUp(670, -600, 40, 40, texture=scaled_double_jump_icon),
                     PowerUp(120, -2400, 40, 40, texture=scaled_double_jump_icon),
                     PowerUp(400, -1200, 40, 40, texture=scaled_double_jump_icon),
                     PowerUp(650, -1470, 40, 40, texture=scaled_double_jump_icon),
    ]

    # Ziel erstellen
    goal1 = Goal(WHITE, 700, -3380, 60, 80,texture=scaled_texture_trophy)
    # Deathzone erstellen
    deathzone1 = Deathzone(WHITE, -1000, 900, 20000, 20000)
    # Spieler erstellen
    player1 = Player(RED, Cx - 300, 500, 50, 50, texture=scaled_image_player1)

    # Hauptspielschleife
    gameactive = True
    global game_running

    game_running = True

    while gameactive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameactive = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu()


        player1.KeyPress()
        camera_offset_y = player1.rect.y - screen_height / 2
        background_scroll_faktor = 0.2
        draw_background(screen, backgrounds, camera_offset_y, background_scroll_faktor)

        #Gegner zeichen
        for enemy in list_enemy:
            enemy.update()
            enemy.draw(screen, camera_offset_y)

        for static_enemy in list_static_enemy:
            static_enemy.draw(screen, camera_offset_y)
        # Plattformen zeichnen
        for platform in list_platform:
            platform.draw(screen, camera_offset_y)
        #Rutsche zeichnen
        for slope in list_slopes:
            slope.draw(screen, camera_offset_y)
        # Coins zeichnen
        for coin in list_ruby_coins:
            coin.draw(screen, camera_offset_y)

        for coin in list_gold_coins:
            coin.draw(screen, camera_offset_y)

        for powerup in list_powerups:
            powerup.check_collision(player1)
            powerup.update()
            powerup.draw(screen, camera_offset_y)

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
        player1.handle_collisions(list_platform, list_slopes)
        player1.rect.topleft = (player1.rect.x, player1.rect.y)
        player1.resetJump()
        powerup.check_collision(player1)
        powerup.update()


        # Coin-Kollision
        for i in range(len(list_ruby_coins)-1, -1, -1):
            if player1.rect.colliderect(list_ruby_coins[i].rect):
                collect = pygame.mixer.Sound(r"Sounds\CoinCollect1.mp3")
                pygame.mixer.Sound.set_volume(collect, 0.1)
                pygame.mixer.Sound.play(collect)
                del list_ruby_coins[i]
                score += 1
        for i in range(len(list_gold_coins)-1, -1, -1):
            if player1.rect.colliderect(list_gold_coins[i].rect):
                collect = pygame.mixer.Sound(r"Sounds\CoinCollect1.mp3")
                pygame.mixer.Sound.set_volume(collect, 0.1)
                pygame.mixer.Sound.play(collect)
                del list_gold_coins[i]
                score += 2

        # Enemy-Kollision
        for enemy in list_enemy:
            if player1.rect.colliderect(enemy.rect):
                if not invincible:
                    invincible = True
                    hitpoints -= 1
                    hitmoment = pygame.time.get_ticks()
                    damage = pygame.mixer.Sound(r"Sounds\damage.mp3")
                    pygame.mixer.Sound.set_volume(damage, 0.5)
                    pygame.mixer.Sound.play(damage)

        for static_enemy in list_static_enemy:
            if player1.rect.colliderect(static_enemy.rect):
                if not invincible:
                    invincible = True
                    hitpoints -= 1
                    hitmoment = pygame.time.get_ticks()
                    damage = pygame.mixer.Sound(r"Sounds\damage.mp3")
                    pygame.mixer.Sound.set_volume(damage, 0.5)
                    pygame.mixer.Sound.play(damage)

        if invincible:
            player1.texture = scaled_image_player1_hit
            player1.f = ORANGE
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - hitmoment

            if (elapsed_time // 50) % 2 == 0:
                player1.texture = scaled_image_player1_hit
            else:
                player1.texture = scaled_image_player1
            if current_time - hitmoment >= 1000:
                player1.texture = scaled_image_player1
                invincible = False
                player1.f = RED
                player1.texture = scaled_image_player1

        # Goal Kollision
        reset_triggered = False

        if player1.rect.colliderect(goal1.rect):
            if not reset_triggered:
                reset_triggered = True  # Reset nur einmal auslösen
                player1 = Player(RED, Cx - 300, 500, 50, 50, texture=scaled_image_player1)
                list_ruby_coins[:] = create_ruby_coins()
                list_gold_coins[:] = create_gold_coins()
                score = 0
                invincible = False
                hitpoints = 3
                victory = pygame.mixer.Sound(r"Sounds\victory1.mp3")
                pygame.mixer.Sound.play(victory)
        else:
            reset_triggered = False

        # Deathzone Kollision
        if player1.rect.colliderect(deathzone1.rect):
            if not reset_triggered:
                reset_triggered = True  # Reset nur einmal auslösen
                player1 = Player(RED, Cx - 25, 450, 50, 50, texture=scaled_image_player1)
                list_ruby_coins[:] = create_ruby_coins()
                list_gold_coins[:] = create_gold_coins()
                score = 0
                invincible = False
                hitpoints = 3
        else:
            reset_triggered = False

        # Spieler-Reset
        if hitpoints <= 0:
            hitpoints = 3
            score = 0
            list_ruby_coins[:] = create_ruby_coins()
            list_gold_coins[:] = create_gold_coins()
            player1 = Player(RED, Cx - 300, 500, 50, 50, texture=scaled_image_player1)

        # Scoreanzeige zeichnen
        score_text = font.render('Score = ' + str(score), True, YELLOW)
        screen.blit(score_text, (37, 65))


        for i in range(hitpoints):
            list_hearts[i].draw(screen, 0)

        #menu button
        button(900, 50, 40, 40, '...', 6, 0, (255,255,255))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# values after 'text' are for centralizing text
def button(x, y, w, h, text, text_offset_x, text_offset_y, color):
    global game_running, gameactive

    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()


    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = font.render((text), True, BLACK)
    screen.blit(button_text, (x + text_offset_x, y + text_offset_y))

    if mouse_pos[0] >= x and mouse_pos[0] <= x + w and mouse_pos[1] >= y and mouse_pos[1] <= y + h:
        pygame.draw.rect(screen, (210, 210, 210), (x, y, w, h))
        screen.blit(button_text, (x + text_offset_x, y + text_offset_y))

        if click[0]:  # Linksklick gedrückt?
            pygame.time.delay(150)  # Kurze Verzögerung für bessere Button-Reaktion
            if text == 'START':
                game_running = True
                start_game()
            elif text == 'RESUME':
                game_running = True
                return
            elif text == 'QUIT':
                pygame.quit()
                exit()
            elif text == 'BACK':
                menu()
            elif text == '...':
                menu()
            elif text == 'RESUME':
                start_game()


def menu():
    global game_running
    game_started = False
    if game_running:
        game_running = False
        game_started = True

    while not game_running:  # Menü läuft nur, wenn das Spiel pausiert ist
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if game_running:  # Falls Resume gedrückt wurde, verlasse das Menü
            return

        button(Cx - 100, Cy-100, 200, 70, 'START' if not game_started else 'RESUME', 50, 20, WHITE)
        #button(Cx - 100, 100, 200, 70, 'RESUME', 40, 20, WHITE)
        #button(Cx - 100, 225, 200, 70, 'Options', 40, 20, WHITE)
        button(Cx - 100, 300, 200, 70, 'QUIT', 60, 20, WHITE)

        pygame.display.update()


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
