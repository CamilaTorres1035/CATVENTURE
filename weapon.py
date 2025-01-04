import pygame
import cons
import math

class Weapon:
    def __init__(self, image, image_bullet):
        self.image_bullet = image_bullet
        self.image_origin = image
        self.angle = 0
        self.image = pygame.transform.rotate(self.image_origin, self.angle)
        self.shape = self.image.get_rect()
        self.shot = False
        self.last_shot = pygame.time.get_ticks()
    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.image, self.angle)
        screen.blit(self.image, self.shape)
        #*pygame.draw.rect(screen, cons.COLOR_WEAPON, self.shape, width=1)
    
    def update(self, player):
        bullet = None
        shot_cooldown = cons.SHOT_COOLDOWN
        
        self.shape.center = player.shape.center
        
        # move with the character
        if player.flip == False:
            self.shape.x = self.shape.x + player.shape.width//8
            self.rotate(False)
        else:
            self.shape.x = self.shape.x - player.shape.width//8
            self.rotate(True)
        self.shape.y = self.shape.y - player.shape.height//10
        
        # move with the mouse
        mouse_pos = pygame.mouse.get_pos()
        diference_x = mouse_pos[0] - self.shape.centerx
        diference_y = -(mouse_pos[1] - self.shape.centery)
        self.angle = math.degrees(math.atan2(diference_y, diference_x))
        
        # detect click
        if pygame.mouse.get_pressed()[0] and self.shot == False and (pygame.time.get_ticks()-self.last_shot >= shot_cooldown):
            bullet = Bullet(self.image_bullet,self.shape.centerx, self.shape.centery, self.angle)
            self.shot = True
            self.last_shot = pygame.time.get_ticks()
        
        # reset click
        if pygame.mouse.get_pressed()[0] == False:
            self.shot = False
        
        return bullet
    
    def rotate(self, rotate):
        if rotate == True:
            image_flip = pygame.transform.flip(self.image_origin, True, False)
            self.image = pygame.transform.rotate(image_flip, self.angle)
        else:
            image_flip = pygame.transform.flip(self.image_origin, False, False)
            self.image = pygame.transform.rotate(image_flip, self.angle)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = image
        self.angle = angle
        self.image = pygame.transform.rotate(self.image_origin, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.delta_x = math.cos(math.radians(self.angle))*cons.SPEED_BULLET
        self.delta_y = -math.sin(math.radians(self.angle))*cons.SPEED_BULLET
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height())))
    
    def update(self):
        self.rect.x = self.rect.x + self.delta_x
        self.rect.y = self.rect.y + self.delta_y
        
        # check if the bullets are off screen
        if self.rect.right < 0 or self.rect.left > cons.WIDTH or self.rect.bottom > cons.HEIGHT or self.rect.top < 0:
            self.kill()