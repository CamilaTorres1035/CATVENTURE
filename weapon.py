import pygame
import cons
import math

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