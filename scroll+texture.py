import pygame
import math

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1000, 600))
screen_width, screen_height = screen.get_size()
Cx, Cy = screen_width / 2, screen_height / 2
v0x, v0y = 5, 5
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)

class Player:
    def __init__(self, farbe, x, y, width, height,texture=None):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.texture = texture
        self.v = pygame.Vector2(v0x, v0y)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.isjump = False
        self.jumpCount = 10
        self.gravity = 0.8
        self.nextjump = 0
        self.jump_cooldown = 1000
        self.isOnPlatform = False

    def draw (self, screen, camera_offset_y):
        if self.texture:
            screen.blit(self.texture, (self.x, self.y - camera_offset_y))
        else:
            pygame.draw.rect(screen, self.f, (self.x, self.y -camera_offset_y, self.w, self.h))

    def KeyPress(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()

        if keys[pygame.K_SPACE] and not self.isjump and (
                current_time - self.nextjump) >= self.jump_cooldown and self.isOnPlatform:
            self.isjump = True
            self.jumpCount = 10
            self.nextjump = current_time
        if keys[pygame.K_d]:
            self.x += self.v[0]
        if keys[pygame.K_a]:
            self.x -= self.v[0]
        self.rect.x = self.x
        self.rect.y = self.y

    def applyGravity(self):
        if not self.isjump:
            self.v[1] += self.gravity
        else:
            self.v[1] = -10
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
    def __init__(self, farbe, x, y, width, height, texture=None):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.texture = texture


    def draw(self, screen, camera_offset_y):
        draw_pos = (self.x, self.y - camera_offset_y)
        if self.texture:
            screen.blit(self.texture, draw_pos)
        else:
            pygame.draw.rect(screen, self.f, [self.x, self.y - camera_offset_y, self.w, self.h])

# Textur laden und skalieren
texture_Boden = pygame.image.load(r"C:\users\phste\OneDrive\Desktop\Bodentextur2.webp")
scaled_texture_floor1 = pygame.transform.scale(texture_Boden, (500, 500))
scaled_texture_floor2 = pygame.transform.scale(texture_Boden, (320, 60 ))
Plattform_texture = pygame.image.load(r"C:\Users\phste\OneDrive\Desktop\Animierte Plattform2.png")
scaled_image_platform = pygame.transform.scale(Plattform_texture, (200,70))
texture_Player1 = pygame.image.load(r"C:\Users\phste\OneDrive\Desktop\Player3.png")
scaled_image_Player1 = pygame.transform.scale(texture_Player1, (52, 52))

# Texturplattformen
platform_floor1 = Platform(SCHWARZ, 0, 570, 500, 500, texture=scaled_texture_floor1)
platform_floor2 = Platform(SCHWARZ, 500, 570, 500, 500, texture=scaled_texture_floor1)
platform1 = Platform(WEISS,640,400,200,30,texture=scaled_image_platform)
platform2 = Platform(WEISS,0,210, 320, 60, texture=scaled_texture_floor2)


list_platform = [
    platform_floor1,
    platform_floor2,
    platform1,
    platform2,
]
player1 = Player(ROT, Cx - 25, 50, 50, 50,texture=scaled_image_Player1)

#Variable für den Kameraoffset in y-Richtung
camera_offset_y = 0

spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    player1.KeyPress()

    # y in Offset sodass Spieler vertikal mittig bleibt: Kamera folgt spieler
    camera_offset_y = player1.y - screen_height / 2

    screen.fill(WEISS)

    # Spieler mit Offset zeichnen
    player1.draw(screen, camera_offset_y)

    # Plattformen mit Offset zeichnen
    for platform in list_platform:
        platform.draw(screen, camera_offset_y)


    player1.applyGravity()
    player1.jump()
    player1.isOnPlatform = False

    # Kollisionen
    for platform in list_platform:
        if player1.rect.colliderect(platform.rect):
            # Kollision von oben
            if (player1.rect.y + player1.rect.h) > platform.rect.y > player1.rect.y:
                player1.y = platform.rect.y - player1.rect.h + 0.5
                player1.v[1] = v0y
                player1.isOnPlatform = True

            # Kollision von unten
            elif player1.rect.y < (platform.rect.y + platform.rect.h) < (player1.rect.y + player1.rect.h):
                player1.y = platform.rect.y + platform.rect.h
                player1.v[1] = v0y

            # Kollision von links
            elif (player1.rect.x + player1.rect.w) > platform.rect.x > player1.rect.x:
                player1.x = platform.rect.x - player1.rect.w
                player1.v[0] = v0x

            # Kollision von rechts
            elif player1.rect.x < (platform.rect.x + platform.rect.w) < (player1.rect.x + player1.rect.w):
                player1.x = platform.rect.x + platform.rect.w
                player1.v[0] = v0x

    player1.resetJump()
    clock.tick(60)
    pygame.display.flip()
