import pygame as pygame
import math

#git add .
#git commit -m "test"
#git push

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1500, 750))
screen_width , screen_height = screen.get_size()
Cx , Cy = screen_width/2 , screen_height/2
v0x, v0y = 5, 5
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)
ORANGE = (255, 140, 0)
GELB = (255, 255, 0)
GRÜN = (0, 255, 0)
BLAU = (0, 0, 255)
Hä = (56, 84, 120)

INVINCIBLE = False
LEBEN = 3

class Player:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.v = pygame.Vector2(v0x, v0y)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.isjump = False
        self.jumpCount = 10
        self.gravity = 1
        self.nextjump = 0
        self.jump_cooldown = 1000
        self.isOnPlatform = False


    def KeyPress(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and not self.isjump and (current_time - self.nextjump) >= self.jump_cooldown and self.isOnPlatform == True:
            self.isjump = True
            self.jumpCount = 10
            self.nextjump = current_time
        if keys[pygame.K_d]:
            self.x += self.v[0]
        if keys[pygame.K_a]:
            self.x -= self.v[0]
        #if keys[pygame.K_s]:
            #self.y += self.v[1]
        self.rect.x = self.x
        self.rect.y = self.y


    def applyGravity(self):
        if not self.isjump:
            self.v[1] += self.gravity
        else:
            self.v[1] = -7.5
        self.y += self.v[1]
        self.rect.y = self.y

    def jump(self):
        if self.isjump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount * 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isjump = False

    def resetJump(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.isjump = False
            self.jumpCount = 10
            self.v[1] = 0



class Platform:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class Gegner:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h) 


class Coin:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x,self.y,self.h,self.w)
    def draw(self):
        self.rect.topleft = (self.x, self.y)
        pygame.draw.rect(screen, GELB, self.rect)

class Goal:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.h, self.w)
    def draw(self):
        self.rect.topleft = (self.x, self.y)
        pygame.draw.rect(screen, Hä, self.rect)

list_Coins = [
Coin(GELB, 500, 75, 15, 15),
Coin(GELB, 400, 180, 15, 15)
]

farbe = [WEISS, SCHWARZ, ROT, ORANGE, GELB, GRÜN, BLAU, Hä]
list_platform = [Platform(SCHWARZ, 320, 455, 640, 50), Platform(SCHWARZ, 500, 100, 100, 80), Platform(SCHWARZ, 400, 200, 100, 80)]
list_gegner = [Gegner(BLAU, Cx - 100, 100, 200, 200)]
player1 = Player(farbe[2], Cx - 320 , 404 , 50, 50)
font = pygame.font.Font('freesansbold.ttf', 32)
score = 0
text = font.render('Score = ' + str(score), True, GRÜN)
textRect = text.get_rect()
textRect.center = (750, 50)
goal1 = Goal(farbe[7], 700, 50, 50, 50)
spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    player1.KeyPress()
    screen.fill(WEISS)
    pygame.draw.rect(screen, player1.f, [player1.x, player1.y, 50, 50])
    pygame.draw.rect(screen, BLAU, [Cx-100, 200, 50, 50])
    goal1.draw()

    for i in range(len(list_Coins) - 1, -1, -1):
        if player1.rect.colliderect(list_Coins[i].rect):
            del list_Coins[i]
            score += 1
            text = font.render('Score = ' + str(score), True, GRÜN)
            textRect = text.get_rect()
            textRect.center = (750, 50)
    player1.applyGravity()
    player1.jump()
    player1.isOnPlatform = False

    # Kollisionen
    for platform in list_platform:
        if player1.rect.colliderect(platform.rect):
            # kollision von oben
            if (player1.rect.y + player1.rect.h) > platform.rect.y  > player1.rect.y:
                player1.y = platform.rect.y - player1.rect.h +0.5
                player1.v[1] = 0
                player1.v[1] = v0y
                player1.isOnPlatform = True

            # kollision von unten
            elif player1.rect.y < (platform.rect.y + platform.rect.h) < (player1.rect.y + player1.rect.h):
                player1.y = platform.rect.y + platform.rect.h
                player1.v[1] = 0
                player1.v[1] = v0y
            # kollision von links
            elif (player1.rect.x + player1.rect.w) > platform.rect.x > player1.rect.x:
                player1.x = platform.rect.x - player1.rect.w
                player1.v[0] = 0
                player1.v[0] = v0x
            # kollision von rechts
            elif player1.rect.x < (platform.rect.x + platform.rect.w) < (player1.rect.x + player1.rect.w):
                player1.x = platform.rect.x + platform.rect.w
                player1.v[0] = 0
                player1.v[0] = v0x

    player1.resetJump()
    for platform in list_platform:
        pygame.draw.rect(screen, platform.f, platform.rect)

    for Coin  in list_Coins:
        pygame.draw.rect(screen, Coin.f, Coin.rect)

    # Kollision Gegner
    if player1.rect.colliderect(list_gegner[0]) and INVINCIBLE == False:
        INVINCIBLE = True
        LEBEN -= 1
        HITMOMENT = pygame.time.get_ticks()
        
    if INVINCIBLE == True:
        player1.f = farbe[3]
        currenttime = pygame.time.get_ticks()
        if (currenttime - HITMOMENT )>= 500:
            INVINCIBLE = False
            player1.f = farbe[2]

    if LEBEN == 0:    
        LEBEN += 3
        player1 = Player(ROT, Cx - 25 , 405 , 50, 50)

    if player1.rect.colliderect(goal1.rect):
        player1 = Player(ROT, Cx - 25, 405, 50, 50)
        pygame.draw.rect(screen, Coin.f, Coin.rect)

    screen.blit(text, textRect)

    clock.tick(60)

    pygame.display.flip()