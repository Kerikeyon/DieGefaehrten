#player class
import pygame
pygame.mixer.init()
v0x, v0y = 5, 5
screen = pygame.display.set_mode((1000, 600))
screen_width, screen_height = screen.get_size()
class Player:
    def __init__(self, color, x, y, width, height, texture=None):
        self.f = color
        self.texture = texture
        self.v = pygame.Vector2(v0x, v0y)
        self.rect = pygame.Rect(x, y, width, height)
        self.isjump = False
        self.jumpCount = 10
        self.gravity = 1
        self.nextjump = 0
        self.jump_cooldown = 500
        self.isOnPlatform = 0
        self.hitslope = 0
        self.jump_sound = pygame.mixer.Sound(r"Sounds\jump1.mp3")
        self.on_left_slope = False
        self.on_right_slope = False
        self.on_slope = False
        self.slope_slide_speed = 0

    def draw(self, screen, camera_offset_y):
        if self.texture:
            screen.blit(self.texture, (self.rect.x, self.rect.y - camera_offset_y))
        else:
            pygame.draw.rect(screen, self.f, (self.rect.x, self.rect.y - camera_offset_y, self.rect.width, self.rect.height))


    def KeyPress(self, ):
        keys = pygame.key.get_pressed()
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and not self.isjump and (current_time - self.nextjump) >= self.jump_cooldown and self.isOnPlatform <1:
            self.isOnPlatform += 1
            self.isjump = True
            self.jumpCount = 10
            self.nextjump = current_time
            self.jump_sound.play()
        if keys[pygame.K_d] and self.on_left_slope == False:
            self.rect.x += self.v[0]
        if keys[pygame.K_a] and self.on_right_slope == False:
            self.rect.x -= self.v[0]
        """if keys[pygame.K_w] and self.on_left_slope == False:
            self.rect.y -= self.v[1]
        if keys[pygame.K_s] and self.on_right_slope == False:
            self.rect.y += self.v[1]"""


    def applyGravity(self):
        if not self.isjump:
            self.v[1] += self.gravity
        else:
            self.v[1] = -9
        self.rect.y += self.v[1]


    def jump(self):
        if self.isjump:
            if self.jumpCount >= -10:
                neg = 1 if self.jumpCount >= 0 else -1
                self.rect.y -= self.jumpCount * 2 * 0.1 * neg
                self.jumpCount -= 1
            else:
                self.isjump = False

    def resetJump(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.isjump = False
            self.jumpCount = 10
            self.v[1] = 0


    def is_on_diagonal_slope(self, slope):
        
        p1, p2, p3 = slope.points  

        min_x = min(p1[0], p3[0])
        max_x = max(p1[0], p3[0])
        max_y = max(p1[1], p3[1])
        min_y = min(p1[1], p3[1])

        height_slope = self.rect.x + min_y - min_x if slope.direction == "right" else -self.rect.right + max_y + min_x
        
        if self.rect.right < min_x or self.rect.left > max_x:
            return False

        if slope.direction == "right":
            height_slope_top = self.rect.x + min_y - min_x 
            height_slope_bottom = self.rect.right + min_y - min_x 
            
            if height_slope_top <= self.rect.bottom and height_slope_bottom >= self.rect.top and self.rect.left >= min_x:
                return True

        if slope.direction == "left":
            height_slope_bottom = -self.rect.x + max_y + min_x 
            height_slope_top = -self.rect.right + max_y + min_x 
            
            if height_slope_top <= self.rect.bottom and height_slope_bottom >= self.rect.top and self.rect.right <= max_x:
                return True

        return False

    def is_on_horizontal_slope(self, slope):
        """Überprüft, ob der Spieler sich tatsächlich auf einer Schräge befindet"""
        p1, p2, p3 = slope.points  # Eckpunkte der Schräge

        # Bestimme die linke und rechte Grenze der Schräge
        min_x = min(p1[0], p3[0])
        max_x = max(p1[0], p3[0])
        max_y = max(p1[1], p3[1])
        #print(min_x, max_x, max_y, self.rect.top, self.rect.bottom, self.rect.left, self.rect.right)
        if self.rect.top <= max_y <= self.rect.bottom and self.rect.right >= min_x and self.rect.left <= max_x:
            return True
        return False

    def is_on_vertical_slope(self, slope):

        p1, p2, p3 = slope.points  # Eckpunkte der Schräge

        # Bestimme die linke und rechte Grenze der Schräge
        min_x = min(p1[0], p3[0])
        max_x = max(p1[0], p3[0])
        min_y = min(p1[1], p3[1])
        max_y = max(p1[1], p3[1])                
        
        if slope.direction == "left" and self.rect.left <= max_x and self.rect.right >= max_x and self.rect.bottom <= max_y and self.rect.top >= min_y:
            return True
        if slope.direction == "right" and self.rect.left <= min_x and self.rect.right >= min_x and self.rect.bottom <= max_y and self.rect.top >= min_y:
            return True
        return False

    def handle_collisions(self, list_platform, list_slopes):
        for platform in list_platform:
            if self.rect.colliderect(platform.rect):
                self.v[1] = 0
                # Kollision von oben
                if (self.rect.y + self.rect.h) > platform.rect.y > self.rect.y:
                    self.on_left_slope = False
                    self.on_right_slope = False
                    self.rect.y = platform.rect.y - self.rect.h + 0.5
                    self.isOnPlatform = 0
                # Kollision von unten
                elif self.rect.y < (platform.rect.y + platform.rect.h) < (self.rect.y + self.rect.h):
                    self.rect.y = platform.rect.y + platform.rect.h
                # Kollision von links
                elif (self.rect.x + self.rect.w) > platform.rect.x > self.rect.x:
                    self.rect.x = platform.rect.x - self.rect.w
                # Kollision von rechts
                elif self.rect.x < (platform.rect.x + platform.rect.w) < (self.rect.x + self.rect.w):
                    self.rect.x = platform.rect.x + platform.rect.w

        for slope in list_slopes:
            
            p1, p2, p3 = slope.points  # Eckpunkte der Schräge

             # Bestimme die linke und rechte Grenze der Schräge
            min_x = min(p1[0], p3[0])
            max_x = max(p1[0], p3[0])
            max_y = max(p1[1], p3[1])
            min_y = min(p1[1], p3[1])

            height_slope = self.rect.x + min_y - min_x if slope.direction == "right" else -self.rect.right + max_y + min_x


            if self.is_on_horizontal_slope(slope) and self.v[1] < 0:
                self.rect.top = max_y 
           
            #self.is_on_horizontal_slope(slope) #temp
            elif self.is_on_horizontal_slope(slope) and self.is_on_diagonal_slope(slope):
                if slope.direction == "left":
                    self.rect.right = min_x
                if slope.direction == "right":
                    self.rect.left = max_x  

            elif self.is_on_diagonal_slope(slope) and self.is_on_vertical_slope(slope):
                self.rect.bottom = min_y

            elif self.is_on_diagonal_slope(slope) and not self.is_on_vertical_slope(slope):
                self.v[1] = 8
                if slope.direction == "left":
                    self.rect.x -= 8
                    self.rect.bottom = height_slope + 1
                elif slope.direction == "right":
                    self.rect.x += 8 
                    self.rect.bottom = height_slope

            elif self.is_on_vertical_slope(slope):
                if slope.direction == "left":
                    self.rect.left = max_x
                if slope.direction == "right":
                    self.rect.right = min_x

            
                  