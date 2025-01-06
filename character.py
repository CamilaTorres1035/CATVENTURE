import pygame
import cons

class Character():
    def __init__(self, x, y, animations, energy, type_character):
        self.score = 0
        self.energy = energy
        self.alive = True
        self.flip = False
        self.animations = animations
        # image of actual animation
        self.frame_index = 0
        
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.type = type_character
        
        
    def draw(self, screen):
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(image_flip, self.shape)
        #*pygame.draw.rect(screen, cons.COLOR_CHARACTER, self.shape, width=1)
    
    def update(self):
        # Check if the character is still alive
        if self.energy <= 0:
            self.energy = 0
            self.alive = False
        
        # time of animation
        cooldown_animation = 80
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
    def movement(self, delta_x, delta_y):
        pos_screen = [0,0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False
        self.shape.x = self.shape.x + delta_x
        self.shape.y = self.shape.y + delta_y
        
        # Player (1)
        if self.type == 1:
            if self.shape.right > (cons.WIDTH - cons.lim_screen):
                pos_screen[0] = (cons.WIDTH - cons.lim_screen) - self.shape.right
                self.shape.right = cons.WIDTH - cons.lim_screen
            if self.shape.left < cons.lim_screen:
                pos_screen[0] = cons.lim_screen - self.shape.left
                self.shape.left = cons.lim_screen
            if self.shape.bottom > (cons.HEIGHT - cons.lim_screen):
                pos_screen[1] = (cons.HEIGHT - cons.lim_screen) - self.shape.bottom
                self.shape.bottom = cons.HEIGHT - cons.lim_screen
            if self.shape.top < cons.lim_screen:
                pos_screen[1] = cons.lim_screen - self.shape.top
                self.shape.top = cons.lim_screen
        
        return pos_screen