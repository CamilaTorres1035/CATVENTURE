import cons
from items import Item
from character import Character
obstacles = [21,22,23,25,27,28,29,31,32,33,35,36,37,41,42,43,45,46,47,49,51,52,53,55,57,61,62,63,65,67,68,69,71,72,73,75,76,77,101,102,103,104,105,109,110,111,113,115,116,117,121,125,141,145,161,165,181,182,183,184,185,189,79]
kill = 79
exit = 174

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacles = []
        self.exit = None
        self.item_list = []
        self.enemy_list = []
    
    def process_data(self, data, tile_list, item_images, character_images, level):
        self.level_len = len(data)
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*cons.TILE_SIZE
                image_y = y*cons.TILE_SIZE
                image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]
                if tile in obstacles:
                    self.obstacles.append(tile_data)
                elif tile == exit:
                    self.exit = tile_data
                elif tile == 177:
                    coin = Item(image_x, image_y, 0, item_images[0])
                    self.item_list.append(coin)
                    tile_data[0] = tile_list[-1]
                    if level == 4:
                        tile_data[0] = tile_list[122]
                elif tile == 178:
                    heart = Item(image_x, image_y, 1, item_images[1])
                    self.item_list.append(heart)
                    tile_data[0] = tile_list[-1]
                    if level == 4:
                        tile_data[0] = tile_list[122]
                elif tile == 210:
                    Bird = Character(image_x, image_y, character_images[0], 100, 2)
                    self.enemy_list.append(Bird)
                    tile_data[0] = tile_list[-1]
                    if level == 4:
                        tile_data[0] = tile_list[122]
                elif tile == 169:
                    Dog = Character(image_x, image_y, character_images[1], 100, 2)
                    self.enemy_list.append(Dog)
                    tile_data[0] = tile_list[-1]
                    if level == 4:
                        tile_data[0] = tile_list[122]
                self.map_tiles.append(tile_data)
    
    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])
    
    def update(self, pos_screen):
        for tile in self.map_tiles:
            tile[2] += pos_screen[0]
            tile[3] += pos_screen[1]
            tile[1].center = (tile[2], tile[3])