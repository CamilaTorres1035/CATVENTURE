import pygame
import cons
from character import Character
from weapon import Bullet
from texts import DamageText
from items import Item
import os

# Functions
def scale_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    image_scaled = pygame.transform.scale(image, (w*scale, h*scale))
    return image_scaled

def count_elements(directory):
    return len(os.listdir(directory))

def list_elements(directory):
    return os.listdir(directory)

# Initialize the game
pygame.init()

# Screen configuration
pygame.display.set_caption('My First Game')
screen = pygame.display.set_mode((cons.WIDTH, cons.HEIGHT))

# Status Images
heart_full = pygame.image.load('assets//images//items//Heart//Heart-1.PNG')
heart_full = scale_img(heart_full, cons.SCALE_HEART)
heart_half = pygame.image.load('assets//images//items//Heart//Heart-2.PNG')
heart_half = scale_img(heart_half, cons.SCALE_HEART)
heart_empty = pygame.image.load('assets//images//items//Heart//Heart-3.PNG')
heart_empty = scale_img(heart_empty, cons.SCALE_HEART)

# Items images and group
heart_images = []
ruta_heart = 'assets//images//items//Heart-2'
num_heart_images = count_elements(ruta_heart)
for i in range(num_heart_images):
    img = pygame.image.load(f'assets//images//items//Heart-2//Heart-{i+1}.png').convert_alpha()
    img = scale_img(img, cons.SCALE_ITEMS)
    heart_images.append(img)

coin_images = []
ruta_coin = 'assets//images//items//Coin'
num_coin_images = count_elements(ruta_coin)
for i in range(num_coin_images):
    img = pygame.image.load(f'assets//images//items//Coin//Coin-{i+1}.png')
    img = scale_img(img, cons.SCALE_ITEMS)
    coin_images.append(img)

group_items = pygame.sprite.Group()

coin = Item(350, 25, 0, coin_images)
heart = Item(380, 38, 1, heart_images)
heart2 = Item(400, 38, 1, heart_images)

group_items.add(coin)
group_items.add(heart)
group_items.add(heart2)

# Text
font = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 25)

group_damage_text = pygame.sprite.Group()

# Configure player
def draw_score(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def life_player():
    h_half_drawn = False
    for i in range(5):
        if player.energy >= ((i+1)*20):
            screen.blit(heart_full, (5+i*50, 5))
        elif player.energy % 20 > 0 and h_half_drawn == False:
            h_half_drawn = True
            screen.blit(heart_half, (5+i*50, 5))
        else:
            screen.blit(heart_empty, (5+i*50, 5))

animations = []
for i in range(1, 11):
    img = pygame.image.load(f'assets//images//characters//Cat//Cat-{i}.png')
    img = scale_img(img, cons.SCALE_CHAR)
    animations.append(img)

player = Character(50, 50, animations, 20)

# Configure enemies
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

Bird = Character(400, 300, animations_enemies[0], 100)
Dog = Character(200, 300, animations_enemies[1], 100)

list_enemies = []
list_enemies.append(Bird)
list_enemies.append(Dog)

# Configure bullet image
image_bullet = pygame.image.load('assets//images//weapons//bullet.png')
image_bullet = scale_img(image_bullet, cons.SCALE_BULLET)

# Bullet group
group_bullets = pygame.sprite.Group()

# Frame rate control
clock = pygame.time.Clock()

# Player movement
move_right = False
move_left = False
move_up = False
move_down = False

running = True

while running:
    clock.tick(cons.FPS)
    screen.fill(cons.COLOR_BG)

    # Draw player
    player.draw(screen)
    player.update()
    
    # Draw enemies
    for enemy in list_enemies:
        enemy.draw(screen)
    
    for enemy in list_enemies:
        enemy.update()
        #*print(enemy.energy)

    # Draw bullets
    for bullet in group_bullets:
        bullet.draw(screen)
        damage, pos_damage = bullet.update(list_enemies)
        if damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, cons.COLOR_GREEN)
            group_damage_text.add(damage_text)
    
    life_player()
    draw_score(f'Score: {player.score}', font, (0,0,0), 700, 5)
    
    group_damage_text.update()
    group_damage_text.draw(screen)
    
    group_items.update(player)
    group_items.draw(screen)

    # Player movement
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

        # Detect keys for movement
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
        
        # Shoot with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = Bullet(image_bullet, player.shape.centerx, player.shape.centery, mouse_x, mouse_y)
            group_bullets.add(bullet)

    pygame.display.update()

pygame.quit()
