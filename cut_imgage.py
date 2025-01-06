from PIL import Image
import os
# 20X11

def cut_image(ruta_image, output_dir, div_col):
    # load image
    img = Image.open(ruta_image)
    # get size of image
    width, height = img.size
    
    # calculate the row size for square images
    size_square = width // div_col
    div_row = height // size_square
    
    # create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # cut the image and save each tile
    count = 0
    for i in range(div_row):
        for j in range(div_col):
            left = j*size_square
            upper = i*size_square
            right = left + size_square
            lower = upper + size_square
            # cut and save it
            tile = img.crop((left, upper, right, lower))
            name_tile = f'tile ({count+1}).png'
            tile.save(os.path.join(output_dir, name_tile))
            count += 1

cut_image('assets/images/tiles/tileset_full.png', 'assets/images/tiles', 20)