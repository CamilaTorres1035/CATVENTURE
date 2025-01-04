import pygame
import cons
import math

import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_origin = image
        self.rect = self.image_origin.get_rect()
        self.rect.center = (x, y)
        self.speed = cons.SPEED_BULLET
        
        # Calcular ángulo hacia el cursor
        angle = math.atan2(target_y - y, target_x - x)
        self.delta_x = math.cos(angle) * self.speed
        self.delta_y = math.sin(angle) * self.speed
        
        # Rotar la imagen de la bala
        self.angle = math.degrees(-angle)
        self.image = pygame.transform.rotate(self.image_origin, self.angle)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        # Mover bala
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        # Eliminar balas fuera de pantalla
        if (self.rect.right < 0 or self.rect.left > cons.WIDTH or 
            self.rect.bottom < 0 or self.rect.top > cons.HEIGHT):
            self.kill()
