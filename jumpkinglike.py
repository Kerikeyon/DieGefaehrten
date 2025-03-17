import pygame as pygame

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((640,480))
spielaktive = True
Cx , Cy = 640/2 , 480/2
dt = 0

class Player:
    def __init__(self):
        self.p = pygame.Vector2(Cx - 25, Cy - 25)

player = Player()


while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    screen.fill('white')

    pygame.draw.rect(screen, 'red', [player.p[0], player.p[1], 50, 50])
    pygame.draw.rect(screen, 'black', [Cx-100, Cy+25, 200, 50])

    clock.tick(60)

    pygame.display.flip()
