import pygame
import cons
from character import Character
from weapon import Bullet
from texts import DamageText
from items import Item
from world import World
import csv
import os

# Functions
def scale_img(image, scale):
    """Scale an image by a given factor."""
    w = image.get_width()
    h = image.get_height()
    image_scaled = pygame.transform.scale(image, (w*scale, h*scale))
    return image_scaled

def count_elements(directory):
    """Count the number of elements in a directory."""
    return len(os.listdir(directory))

def list_elements(directory):
    """List the elements in a directory."""
    return os.listdir(directory)

# Initialize the game
pygame.init()

# Screen configuration
pygame.display.set_caption('My First Game')
screen = pygame.display.set_mode((cons.WIDTH, cons.HEIGHT))

# Load background images
BackGround = []
for i in range(3):
    img = pygame.image.load(f'assets/images/backround/background-{i+1}.png')
    img = pygame.transform.scale(img, (cons.WIDTH, cons.HEIGHT))
    BackGround.append(img)

pos_screen = [0, 0]

# Load status images
heart_full = pygame.image.load('assets//images//items//Heart//Heart-1.PNG')
heart_full = scale_img(heart_full, cons.SCALE_HEART)
heart_half = pygame.image.load('assets//images//items//Heart//Heart-2.PNG')
heart_half = scale_img(heart_half, cons.SCALE_HEART)
heart_empty = pygame.image.load('assets//images//items//Heart//Heart-3.PNG')
heart_empty = scale_img(heart_empty, cons.SCALE_HEART)

# Load item images and create item group
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

# Load font for text
font = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 25)

# Create group for damage text
group_damage_text = pygame.sprite.Group()

# Load world data from CSV
World_data = []
for row in range(cons.ROWS):
    rows = [7] * cons.COLUMS
    World_data.append(rows)

with open('levels//map-1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for x, row in enumerate(reader):
        for y, column in enumerate(row):
            World_data[x][y] = int(column)

# Load tile images
tile_list = []
for x in range(cons.TILE_TYPES):
    tile_image = pygame.image.load(f'assets//images//tiles//tile ({x+1}).png')
    tile_image = pygame.transform.scale(tile_image, (cons.TILE_SIZE, cons.TILE_SIZE))
    tile_list.append(tile_image)

# Create world
world = World()
world.process_data(World_data, tile_list)

# Function to draw grid
def draw_grid():
    """Draw a grid on the screen."""
    for x in range(30):
        pygame.draw.line(screen, cons.COLOR_WHITE, (x*cons.TILE_SIZE, 0), (x*cons.TILE_SIZE, cons.HEIGHT))
        pygame.draw.line(screen, cons.COLOR_WHITE, (0, x*cons.TILE_SIZE), (cons.WIDTH, x*cons.TILE_SIZE))

# Function to draw score
def draw_score(text, font, color, x, y):
    """Draw the score on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Function to draw player's life
def life_player():
    """Draw the player's life on the screen."""
    h_half_drawn = False
    for i in range(5):
        if player.energy >= ((i+1)*20):
            screen.blit(heart_full, (5+i*50, 5))
        elif player.energy % 20 > 0 and h_half_drawn == False:
            h_half_drawn = True
            screen.blit(heart_half, (5+i*50, 5))
        else:
            screen.blit(heart_empty, (5+i*50, 5))

# Load player animations
animations = []
for i in range(1, 11):
    img = pygame.image.load(f'assets//images//characters//Cat//Cat-{i}.png')
    img = scale_img(img, cons.SCALE_CHAR)
    animations.append(img)

# Create player
player = Character(80, 320, animations, 20, 1)

# Load enemy animations
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

# Create enemies
Bird = Character(400, 320, animations_enemies[0], 100, 2)
Dog = Character(200, 280, animations_enemies[1], 100, 2)
list_enemies = [Bird, Dog]

# Load bullet image
image_bullet = pygame.image.load('assets//images//weapons//bullet.png')
image_bullet = scale_img(image_bullet, cons.SCALE_BULLET)

# Create bullet group
group_bullets = pygame.sprite.Group()

# Frame rate control
clock = pygame.time.Clock()

# Player movement flags
move_right = False
move_left = False
move_up = False
move_down = False

# Main game loop
running = True
while running:
    clock.tick(cons.FPS)
    screen.fill(cons.COLOR_WHITE)
    for BG in BackGround:
        screen.blit(BG, (0, 0))
    
    draw_grid()
    world.draw(screen)
    world.update(pos_screen)

    # Draw player
    player.draw(screen)
    player.update()
    
    # Draw enemies
    for enemy in list_enemies:
        enemy.enemies(pos_screen)
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
    draw_score(f'Score: {player.score}', font, (0, 0, 0), 700, 5)
    
    group_damage_text.update()
    group_damage_text.draw(screen)
    
    group_items.update(pos_screen, player)
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

    pos_screen = player.movement(delta_x, delta_y)

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
