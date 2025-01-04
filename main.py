import pygame
import cons
from character import Character
from weapon import Weapon

# Initialize the game
pygame.init()

# Set up the screen
pygame.display.set_caption('My First Game')
screen = pygame.display.set_mode((cons.WIDTH, cons.HEIGHT))

def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    image_scaled = pygame.transform.scale(image, (w*scale, h*scale))
    return image_scaled

# Set player
animations = []
for i in range(1,11):
    img = pygame.image.load(f'assets//images//characters//Cat//Cat-{i}.png')
    img = scale_img(img, cons.SCALE_CHAR)
    animations.append(img)

player = Character(50, 50, animations)

# Set weapon
image_bullet = pygame.image.load(f'assets//images//weapons//bullet.png')
image_bullet = scale_img(image_bullet, cons.SCALE_BULLET)

image_gun = pygame.image.load(f'assets//images//weapons//gun.png')
image_gun = scale_img(image_gun, cons.SCALE_WEPON)
gun = Weapon(image_gun, image_bullet)

# Create a group of sprites (gestion balas)
group_bullets = pygame.sprite.Group()

# Set clock (for the control of the frame rate)
clock = pygame.time.Clock()

# Set player movements
move_right = False
move_left = False
move_up = False
move_down = False

# Set Loop
running = True

while running:
    # Control del frame rate
    clock.tick(cons.FPS)
    
    screen.fill(cons.COLOR_BG)
    
    # Mostrar el jugador
    player.draw(screen)
    # actualiza el estado del jugador
    player.update()
    
    # Mostrar el arma 
    gun.draw(screen)
    
    # Mostrar balas
    for bullet in group_bullets:
        bullet.draw(screen)

    # actualiza el estado del arma (balas)
    bullet = gun.update(player)
    if bullet:
        group_bullets.add(bullet)
    
    for bullet in group_bullets:
        bullet.update()
    
    # Calcular el moviviento del jugador
    delta_x = 0
    delta_y = 0
    
    if move_right == True:
        delta_x = cons.SPEED
    if move_left == True:
        delta_x = -cons.SPEED
    if move_up == True:
        delta_y = -cons.SPEED
    if move_down == True:
        delta_y = cons.SPEED
        
    # Mover al jugador
    player.movement(delta_x, delta_y)
    
    for event in pygame.event.get():
        # Cerrar el juego
        if event.type == pygame.QUIT:
            running = False
            
        # Reconocer al presionar una tecla
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_down = True
                
        # Reconocer al soltar una tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_down = False
    
    pygame.display.update()

pygame.quit()
