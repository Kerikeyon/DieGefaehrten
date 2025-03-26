import pygame

class WinScreen:
    def __init__(self, x, y, width, height, texture=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture = texture
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def draw(self, screen, camera_offset_y):
        if not self.texture:
            if self.texture:
                screen.blit(self.texture, (self.x, self.y - camera_offset_y))
            else:
                pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y - camera_offset_y, self.width, self.height))