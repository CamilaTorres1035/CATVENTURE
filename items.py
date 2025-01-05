import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type, animations):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type # 0 = monedad, 1 = corazon
        self.animations = animations
        self.frame_index = 0
        self.time = pygame.time.get_ticks()
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    
    def update(self):
        cooldown_animations = 80
        self.image = self.animations[self.frame_index]
        
        if pygame.time.get_ticks() - self.time > cooldown_animations:
            self.frame_index += 1
            self.time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        