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

# Function to draw score
def draw_text(text, font, color, x, y):
    """Draw the score on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Initialize the game
pygame.init()
pygame.mixer.init()

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
level = 1

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

item_images = [coin_images, heart_images]

group_items = pygame.sprite.Group()


# Load font for text
font = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 25)
font_game_over = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 100)
font_restart = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 30)
font_start = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 50)
font_title = pygame.font.Font('assets//fonts//ThaleahFat.ttf', 100)

game_over_text = font_game_over.render('GAME OVER', True, cons.COLOR_RED)
restart_text = font_restart.render('Restart', True, cons.COLOR_BLACK)

# Start screen
BG_title = pygame.Rect(cons.WIDTH/2 - 240, cons.HEIGHT/2 - 200, 550, 100)
BG_win = pygame.Rect(cons.WIDTH/2 - 240, cons.HEIGHT/2 - 200, 400, 100)
text_start = font_start.render('Start', True, cons.COLOR_WHITE)
text_exit = font_start.render('Exit', True, cons.COLOR_WHITE)
play_button = pygame.Rect(cons.WIDTH/2 - 100, cons.HEIGHT/2 - 50, 200, 50)
exit_button = pygame.Rect(cons.WIDTH/2 - 100, cons.HEIGHT/2 + 50, 200, 50)

def start_screen():
    """Draw the start screen."""
    screen.fill(cons.COLOR_WHITE)
    for BG in BackGround:
        screen.blit(BG, (0, 0))
    pygame.draw.rect(screen, cons.COLOR_BG, BG_title)
    draw_text('CATVENTURE', font_title, cons.COLOR_YELLOW, cons.WIDTH/2 - 200, cons.HEIGHT/2 - 200)
    pygame.draw.rect(screen, cons.COLOR_GREEN, play_button)
    pygame.draw.rect(screen, cons.COLOR_RED, exit_button)
    screen.blit(text_start, (play_button.x + 50, play_button.y + 5))
    screen.blit(text_exit, (exit_button.x + 60, exit_button.y + 5))
    pygame.display.update()

# Winning screen
def win_screen():
    """Draw the winning screen."""
    screen.fill(cons.COLOR_WHITE)
    for BG in BackGround:
        screen.blit(BG, (0, 0))
    pygame.draw.rect(screen, cons.COLOR_BG, BG_win)
    draw_text('YOU WIN', font_title, cons.COLOR_YELLOW, cons.WIDTH/2 - 200, cons.HEIGHT/2 - 200)
    pygame.draw.rect(screen, cons.COLOR_GREEN, play_button)
    pygame.draw.rect(screen, cons.COLOR_RED, exit_button)
    screen.blit(text_start, (play_button.x + 50, play_button.y + 5))
    screen.blit(text_exit, (exit_button.x + 60, exit_button.y + 5))
    pygame.display.update()
# Create group for damage text
group_damage_text = pygame.sprite.Group()

# Load world data from CSV
def reset_world():
    group_damage_text.empty()
    group_bullets.empty()
    group_items.empty()
    data = []
    for row in range(cons.ROWS):
        rows = [7] * cons.COLUMS
        data.append(rows)
    return data

World_data = []
for row in range(cons.ROWS):
    rows = [7] * cons.COLUMS
    World_data.append(rows)

with open('levels//map-1.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, column in enumerate(row):
            World_data[x][y] = int(column)

# Load tile images
tile_list = []
for x in range(cons.TILE_TYPES):
    tile_image = pygame.image.load(f'assets//images//tiles//tile ({x+1}).png')
    tile_image = pygame.transform.scale(tile_image, (cons.TILE_SIZE, cons.TILE_SIZE))
    tile_list.append(tile_image)


# Function to draw grid
def draw_grid():
    """Draw a grid on the screen."""
    for x in range(30):
        pygame.draw.line(screen, cons.COLOR_WHITE, (x*cons.TILE_SIZE, 0), (x*cons.TILE_SIZE, cons.HEIGHT))
        pygame.draw.line(screen, cons.COLOR_WHITE, (0, x*cons.TILE_SIZE), (cons.WIDTH, x*cons.TILE_SIZE))


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
player = Character(200, 200, animations, 100, 1)

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

list_enemies = []

# Create world
world = World()
world.process_data(World_data, tile_list, item_images, animations_enemies)

# Add items to group
for item in world.item_list:
    group_items.add(item)

# Add enemies to list
for enemy in world.enemy_list:
    list_enemies.append(enemy)

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
pygame.mixer.music.load('assets//sounds//game-music-loop.mp3')
pygame.mixer.music.play(-1)

sound_shot = pygame.mixer.Sound('assets//sounds//game-shot.mp3')

show_start_screen = True
running = True
while running:
    if show_start_screen:
        start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    show_start_screen = False
                if exit_button.collidepoint(event.pos):
                    running = False
        continue
    clock.tick(cons.FPS)
    screen.fill(cons.COLOR_WHITE)
    for BG in BackGround:
        screen.blit(BG, (0, 0))
    
    world.draw(screen)
    world.update(pos_screen)
    
    if player.alive:
        # Draw player
        player.draw(screen)
        player.update(list_enemies)
        
        # Draw enemies
        for enemy in list_enemies:
            if enemy.alive == False:
                player.score += 5
                list_enemies.remove(enemy)
                continue
            enemy.enemies(pos_screen)
            enemy.draw(screen)
        
        for enemy in list_enemies:
            enemy.update()

        # Draw bullets
        for bullet in group_bullets:
            sound_shot.play()
            bullet.draw(screen)
            damage, pos_damage = bullet.update(list_enemies, world.obstacles)
            if damage:
                damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font, cons.COLOR_GREEN)
                group_damage_text.add(damage_text)
        
        life_player()
        draw_text(f'Score: {player.score}', font, cons.COLOR_BLACK, 650, 5)
        
        draw_text(f'Level: {level}', font, cons.COLOR_BLACK, cons.WIDTH/2, 5)
        
        group_damage_text.update(pos_screen)
        group_damage_text.draw(screen)
        
        # Draw items
        group_items.update(pos_screen, player)
        group_items.draw(screen)

        # Player movement
        delta_x = 0

        if move_right:
            delta_x = cons.SPEED
        if move_left:
            delta_x = -cons.SPEED

        pos_screen, level_end = player.movement(delta_x, world.obstacles, world.exit)
        
        if level_end:
            if player.alive and level == cons.FINAL_LEVEL:
                win_screen()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button.collidepoint(event.pos):
                            show_start_screen = True
                            player.alive = False
                        if exit_button.collidepoint(event.pos):
                            running = False
                continue
            if level < cons.FINAL_LEVEL:
                level += 1
                World_data = reset_world()
                with open(f'levels//map-{level}.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, column in enumerate(row):
                            World_data[x][y] = int(column)
                world = World()
                world.process_data(World_data, tile_list, item_images, animations_enemies)
                player.actualize_coor(cons.COOR_LEVELS[str(level)])
                list_enemies = []
                for enemy in world.enemy_list:
                    list_enemies.append(enemy)
                group_items.empty()
                for item in world.item_list:
                    group_items.add(item)
    
    if player.alive == False:
        screen.fill(cons.COLOR_BLACK)
        screen.blit(game_over_text, (cons.WIDTH/2 - game_over_text.get_width()/2, cons.HEIGHT/2 - game_over_text.get_height()/2))
        restart_button = pygame.Rect(cons.WIDTH/2 - 100, cons.HEIGHT/2 + 100, 200, 50)
        pygame.draw.rect(screen, cons.COLOR_YELLOW, restart_button)
        screen.blit(restart_text, (restart_button.x + 50, restart_button.y + 10))
    
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
                player.perform_jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

        # Shoot with mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            bullet = Bullet(image_bullet, player.shape.centerx, player.shape.centery, mouse_x, mouse_y)
            group_bullets.add(bullet)
        
        # Restart game
        if event.type == pygame.MOUSEBUTTONDOWN and player.alive == False:
            if restart_button.collidepoint(event.pos) and not player.alive:
                player.alive = True
                player.energy = 100
                player.score = 0
                level = 1
                World_data = reset_world()
                with open(f'levels//map-{level}.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, column in enumerate(row):
                            World_data[x][y] = int(column)
                world = World()
                world.process_data(World_data, tile_list, item_images, animations_enemies)
                player.actualize_coor(cons.COOR_LEVELS[str(level)])
                list_enemies = []
                for enemy in world.enemy_list:
                    list_enemies.append(enemy)
                group_items.empty()
                for item in world.item_list:
                    group_items.add(item)
                

    pygame.display.update()

pygame.quit()
