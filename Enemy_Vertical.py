#enemy class
import pygame
class Enemy_Vertical:
    def __init__(self, color, x, y, width, height, speed = 3, movrange = 150, texture = None):
        self.f = color
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.speed = speed  
        self.start_y = y  
        self.movrange = movrange  
        self.direction = 1          
        self.texture = texture        
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h) 



    def update(self):

        self.y += self.speed * self.direction
        self.rect.y = self.y

        if self.y > self.start_y + self.movrange or self.y < self.start_y - self.movrange:
            self.direction *= -1


    def draw(self, screen, camera_offset_y):

        draw_pos = (self.x, self.y - camera_offset_y)
        if self.texture:
            screen.blit(self.texture, draw_pos)
        else:
            pygame.draw.rect(screen, self.f, [self.x, self.y - camera_offset_y, self.w, self.h])
