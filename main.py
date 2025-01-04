import pygame
import cons
from character import Character
from weapon import Bullet
import os

# Funciones
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    image_scaled = pygame.transform.scale(image, (w*scale, h*scale))
    return image_scaled

def count_elements(directory):
    return len(os.listdir(directory))

def list_elements(directory):
    return os.listdir(directory)

# Inicializar el juego
pygame.init()

# Configuración de pantalla
pygame.display.set_caption('My First Game')
screen = pygame.display.set_mode((cons.WIDTH, cons.HEIGHT))

# Configurar jugador
animations = []
for i in range(1, 11):
    img = pygame.image.load(f'assets//images//characters//Cat//Cat-{i}.png')
    img = scale_img(img, cons.SCALE_CHAR)
    animations.append(img)

player = Character(50, 50, animations)

# Configurar enemigos
directory_enemies = 'assets//images//characters//enemies'
type_enemies = list_elements(directory_enemies)

animations_enemies = []
for enemy in type_enemies:
    list_temp = []
    ruta_temp = f'assets//images//characters//enemies//{enemy}'
    num_animations = count_elements(ruta_temp)
    for i in range(num_animations):
        img_enemy = pygame.image.load(f'{ruta_temp}//{enemy}-{i+1}.png')
        img_enemy = scale_img(img_enemy, cons.SCALE_ENEMY)
        list_temp.append(img_enemy)
    animations_enemies.append(list_temp)

Bird = Character(400, 300, animations_enemies[0])
Dog = Character(200, 300, animations_enemies[1])

list_enemies = []
list_enemies.append(Bird)
list_enemies.append(Dog)

# Configurar imagen de bala
image_bullet = pygame.image.load('assets//images//weapons//bullet.png')
image_bullet = scale_img(image_bullet, cons.SCALE_BULLET)

# Grupo de balas
group_bullets = pygame.sprite.Group()

# Control de frame rate
clock = pygame.time.Clock()

# Movimiento del jugador
move_right = False
move_left = False
move_up = False
move_down = False

running = True

while running:
    clock.tick(cons.FPS)
    screen.fill(cons.COLOR_BG)

    # Dibujar jugador
    player.draw(screen)
    player.update()
    
    # Dibujar enemigos
    for enemy in list_enemies:
        enemy.draw(screen)
        enemy.update()

    # Dibujar balas
    for bullet in group_bullets:
        bullet.draw(screen)
        bullet.update()

    # Movimiento del jugador
    delta_x = 0
    delta_y = 0

    if move_right:
        delta_x = cons.SPEED
    if move_left:
        delta_x = -cons.SPEED
    if move_up:
        delta_y = -cons.SPEED
    if move_down:
        delta_y = cons.SPEED

    player.movement(delta_x, delta_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Detectar teclas para movimiento
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_UP:
                move_up = False
            if event.key == pygame.K_DOWN:
                move_down = False
        
        # Disparar con el clic del mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = Bullet(image_bullet, player.shape.centerx, player.shape.centery, mouse_x, mouse_y)
            group_bullets.add(bullet)

    pygame.display.update()

pygame.quit()
