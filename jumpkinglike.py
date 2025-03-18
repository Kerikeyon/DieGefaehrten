import pygame as pygame

#git add .
#git commit -m "test"
#git push

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
screen_width , screen_height = screen.get_size()
Cx , Cy = screen_width/2 , screen_height/2
v0x, v0y = 5, 5
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
ROT = (255, 0, 0)

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

    def KeyPress(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x += self.v[0]
        if keys[pygame.K_a]:
            self.x -= self.v[0]
        if keys[pygame.K_w]:
            self.y -= self.v[1]
        if keys[pygame.K_s]:
            self.y += self.v[1]
        self.rect.x = self.x
        self.rect.y = self.y

    def gravity(self):
        self.y += 3.2
        if self.rect.y > screen_height and self.y >= 0:
            self.y = 0
            self.rect.y = screen_height -self.y -self.y
    def jump(self):
        if self.isjump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.y -= self.jumpCount ** 2 * 0.1 * neg
                self.jumpCount -= 1

class Platform:
    def __init__(self, farbe, x, y, width, height):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

list_platform = [Platform(SCHWARZ, Cx - 320, 455, 640, 50), Platform(SCHWARZ, 300, 100, 100, 80)]
player1 = Player(ROT, Cx - 25 , 50 , 50, 50)

spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    player1.KeyPress()
    screen.fill(WEISS)

    pygame.draw.rect(screen, ROT, [player1.x, player1.y, 50, 50])
    for platform in list_platform:
        pygame.draw.rect(screen, platform.f, platform.rect)

    player1.gravity()

    # Kollisionen
    for platform in list_platform:
        if player1.rect.colliderect(platform.rect):
            # kollision von oben
            if (player1.rect.y + player1.rect.h) > platform.rect.y  > player1.rect.y:
                player1.y = platform.rect.y - player1.rect.h +0.5
                player1.v[1] = 0
                player1.v[1] = v0y
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

    clock.tick(60)

    pygame.display.flip()

