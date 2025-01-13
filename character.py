import pygame
import cons

class Character():
    def __init__(self, x, y, animations, energy, type_character):
        self.score = 0
        self.energy = energy
        self.alive = True
        self.flip = False
        self.animations = animations
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animations[self.frame_index]
        self.shape = self.image.get_rect()
        self.shape.center = (x, y)
        self.type = type_character
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.invulnerable = False
        self.invulnerable_time = 0
        self.invulnerable_duration = 2000  # 2 seconds of invulnerability

    def draw(self, screen):
        # Flip the image if needed and draw it on the screen
        image_flip = pygame.transform.flip(self.image, self.flip, False)
        screen.blit(image_flip, self.shape)

    def enemies(self, pos_screen):
        # Update the character's position based on the screen position
        self.shape.x += pos_screen[0]
        self.shape.y += pos_screen[1]

    def update(self, enemies = []):
        # Check if the character is alive
        if self.energy <= 0:
            self.energy = 0
            self.alive = False

        # Animation cooldown
        cooldown_animation = 80
        self.image = self.animations[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animations):
            self.frame_index = 0
        
        current_time = pygame.time.get_ticks()
        if self.invulnerable and current_time - self.invulnerable_time > self.invulnerable_duration:
            self.invulnerable = False

        if not self.invulnerable:
            for enemy in enemies:
                if self.shape.colliderect(enemy.shape):
                    self.energy -= 20  # Reduce energy by 20 
                    if self.energy < 0:
                        self.energy = 0
                    self.invulnerable = True
                    self.invulnerable_time = current_time
                    break

    def movement(self, delta_x, obstacles, exit_tile):
        level_end = False
        pos_screen = [0, 0]
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        # Horizontal movement
        self.shape.x += delta_x
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.shape):
                if delta_x > 0:
                    self.shape.right = obstacle[1].left
                if delta_x < 0:
                    self.shape.left = obstacle[1].right

        # Increase vertical velocity due to gravity
        if self.vel_y > 0:  # If falling
            self.vel_y += cons.GRAVITY * 1.5  # Multiplier for fast fall
        else:  # If rising or at rest
            self.vel_y += cons.GRAVITY

        # Limit terminal velocity
        if self.vel_y > cons.TERMINAL_VELOCITY:
            self.vel_y = cons.TERMINAL_VELOCITY

        # Update vertical position
        self.shape.y += self.vel_y

        # Check vertical collisions
        for obstacle in obstacles:
            if obstacle[1].colliderect(self.shape):
                if self.vel_y > 0:  # If falling
                    self.shape.bottom = obstacle[1].top
                    self.vel_y = 0
                    self.in_air = False
                elif self.vel_y < 0:  # If rising
                    self.shape.top = obstacle[1].bottom
                    self.vel_y = 0

        # Adjust position at the edges of the screen
        if self.type == 1:
            if exit_tile[1].colliderect(self.shape):
                level_end = True
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

        return pos_screen, level_end
    
    def actualize_coor(self, pos_screen):
        self.shape.center = (pos_screen[0], pos_screen[1])

    def perform_jump(self):
        # Jump control
        if not self.in_air:
            self.vel_y = -25  # Jump force
            self.in_air = True 
