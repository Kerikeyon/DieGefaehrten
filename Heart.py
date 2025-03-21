#heart class
import pygame
class Heart:
    def __init__(self, farbe, x, y, width, height, texture=None):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.texture = texture
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
    def draw(self, screen, camera_offset_y):
        if self.texture:
            screen.blit(self.texture, (self.x, self.y - camera_offset_y))
        else:
            pygame.draw.rect(screen, self.f, (self.x, self.y - camera_offset_y, self.w, self.h))
