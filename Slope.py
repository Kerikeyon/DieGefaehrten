#Slope Klasse
import pygame

class Slope:
    def __init__(self, color, x, y, size, direction, texture=None):
        self.f = color
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.texture = texture
        self.points = self.calculate_points()

    def calculate_points(self):
        if self.direction == "left":
            vector = 1
        if self.direction == "right":
            vector = -1
        
        corner1 = [self.x, self.y]
        corner2 = [self.x, self.y + self.size]
        corner3 = [self.x - self.size * vector, self.y + self.size]
        
        return [corner1, corner2, corner3]


    def draw(self, screen, camera_offset_y):
        draw_points = [[p[0], p[1] - camera_offset_y] for p in self.points]

        if self.texture:
            screen.blit(self.texture, draw_points[0])
        else:
            pygame.draw.polygon(screen, self.f, draw_points)