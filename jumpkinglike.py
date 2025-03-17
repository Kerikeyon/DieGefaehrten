import pygame as pygame

pygame.init()
Weiss  = ( 255, 255, 255)
x = 50
y = 50
width = 40
height = 60
vel = 10
pygame.display.set_mode((640,480))
spielaktive = True
while spielaktive:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            spielaktive = False

    keys = pygame.key.get_pressed()
