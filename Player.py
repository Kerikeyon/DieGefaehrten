#player class
import pygame
v0x, v0y = 5, 5
screen = pygame.display.set_mode((1000, 600))
screen_width, screen_height = screen.get_size()
class Player:
    def __init__(self, farbe, x, y, width, height, texture=None):
        self.f = farbe
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.texture = texture
        self.v = pygame.Vector2(v0x, v0y)
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.isjump = False
        self.jumpCount = 10
        self.gravity = 1
        self.nextjump = 0
        self.jump_cooldown = 500
        self.isOnPlatform = 0

    def draw(self, screen, camera_offset_y):
        if self.texture:
            screen.blit(self.texture, (self.x, self.y - camera_offset_y))
        else:
            pygame.draw.rect(screen, self.f, (self.x, self.y - camera_offset_y, self.w, self.h))

    def KeyPress(self):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and not self.isjump and (current_time - self.nextjump) >= self.jump_cooldown and self.isOnPlatform <2:
            self.isOnPlatform += 1
            self.isjump = True
            self.jumpCount = 10
            self.nextjump = current_time
        if keys[pygame.K_d]:
            self.x += self.v[0]
        if keys[pygame.K_a]:
            self.x -= self.v[0]
        self.rect.x = self.x
        self.rect.y = self.y

    def applyGravity(self):
        if not self.isjump:
            self.v[1] += self.gravity
        else:
            self.v[1] = -9
        self.y += self.v[1]
        self.rect.y = self.y

    def jump(self):
        if self.isjump:
            if self.jumpCount >= -10:
                neg = 1 if self.jumpCount >= 0 else -1
                self.y -= self.jumpCount * 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isjump = False

    def resetJump(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.isjump = False
            self.jumpCount = 10
            self.v[1] = 0