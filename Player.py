#player class
import pygame
pygame.mixer.init()
v0x, v0y = 5, 5
screen = pygame.display.set_mode((1000, 600))
screen_width, screen_height = screen.get_size()
class Player:
    def __init__(self, color, x, y, width, height, texture=None):
        self.f = color
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
        self.jump_sound = pygame.mixer.Sound(r"Sounds\jump1.mp3")
        self.on_slope = False
        self.slope_slide_speed = 0

    def draw(self, screen, camera_offset_y):
        if self.texture:
            screen.blit(self.texture,(self.x, self.y - camera_offset_y))
        else:
            pygame.draw.rect(screen, self.f, (self.x, self.y - camera_offset_y, self.w, self.h))


    def KeyPress(self, ):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and not self.isjump and (current_time - self.nextjump) >= self.jump_cooldown and self.isOnPlatform <1:
            self.isOnPlatform += 1
            self.isjump = True
            self.jumpCount = 10
            self.nextjump = current_time
            self.jump_sound.play()
        if keys[pygame.K_d]:
            self.x += self.v[0]
        if keys[pygame.K_w]:
            self.y -= self.v[1]
        if keys[pygame.K_s]:
            self.y += self.v[1]
        if keys[pygame.K_a]:
            self.x -= self.v[0]
        self.rect.x = self.x
        self.rect.y = self.y


    """def applyGravity(self):
        if not self.isjump:
            self.v[1] += self.gravity
        else:
            self.v[1] = -9
        self.y += self.v[1]
        self.rect.y = self.y"""


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

    def handle_collisions(self, list_platform):
        for platform in list_platform:
            if self.rect.colliderect(platform.rect):
                self.v[1] = 0
                # Kollision von oben
                if (self.rect.y + self.rect.h) > platform.rect.y > self.rect.y:
                    self.y = platform.rect.y - self.rect.h + 0.5
                    self.isOnPlatform = 0
                # Kollision von unten
                elif self.rect.y < (platform.rect.y + platform.rect.h) < (self.rect.y + self.rect.h):
                    self.y = platform.rect.y + platform.rect.h
                # Kollision von links
                elif (self.rect.x + self.rect.w) > platform.rect.x > self.rect.x:
                    self.x = platform.rect.x - self.rect.w
                # Kollision von rechts
                elif self.rect.x < (platform.rect.x + platform.rect.w) < (self.rect.x + self.rect.w):
                    self.x = platform.rect.x + platform.rect.w