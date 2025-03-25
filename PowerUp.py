import pygame
import time

class PowerUp:
    def __init__(self, x, y, width, height, texture=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.texture = texture
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collected = False
        self.respawn_time = 3  # Sekunden
        self.last_collected_time = 0

    def draw(self, screen, camera_offset_y):
        if not self.collected:
            if self.texture:
                screen.blit(self.texture, (self.x, self.y - camera_offset_y))
            else:
                pygame.draw.rect(screen, (0, 255, 255), (self.x, self.y - camera_offset_y, self.width, self.height))

    def check_collision(self, player):
        if not self.collected and self.rect.colliderect(player.rect):
            self.collected = True
            self.last_collected_time = time.time()
            player.isOnPlatform -= 1

    def update(self):
        if self.collected and (time.time() - self.last_collected_time >= self.respawn_time):
            self.collected = False
