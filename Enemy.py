#enemy class
import pygame
class Gegner:
    def __init__(self, farbe, x, y, width, height, speed = 3, bewegungsbereich = 200, texture = None):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.speed = speed  
        self.start_x = x  
        self.bewegungsbereich = bewegungsbereich  
        self.richtung = 1          
        self.texture = texture        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h) 



    def update(self):

        self.x += self.speed * self.richtung
        self.rect.x = self.x

        if self.x > self.start_x + self.bewegungsbereich or self.x < self.start_x - self.bewegungsbereich:
            self.richtung *= -1


    def draw(self, screen, camera_offset_y):

        draw_pos = (self.x, self.y - camera_offset_y)
        if self.texture:
            screen.blit(self.texture, draw_pos)
        else:
            pygame.draw.rect(screen, self.f, [self.x, self.y - camera_offset_y, self.w, self.h])
