import pygame as pygame

#git add .
#git commit -m "test"
#git push

pygame.init()
clock = pygame.time.Clock()
screenX = 640
screenY = 480
screen = pygame.display.set_mode((screenX,screenY))
Cx , Cy = 640/2 , 480/2

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
        self.v = pygame.Vector2(5,5)
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
        if self.rect.y > screenY and self.y >= 0:
            self.y = 0
            self.rect.y = screenY -self.y -self.y
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

list_platform = [Platform(SCHWARZ, Cx - 320, 455, 640, 50)]
player1 = Player(ROT, Cx - 25 , 405 , 50, 50)

spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    player1.KeyPress()
    screen.fill(WEISS)

    pygame.draw.rect(screen, ROT, [player1.x, player1.y, 50, 50])
    pygame.draw.rect(screen, SCHWARZ, [Cx-320, 455, 640, 50])

    player1.gravity()

    clock.tick(60)

    pygame.display.flip()

if player1.rect.colliderect(list_platform[0]):
    print('Ja')
