import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('Icons/png', exist_ok=True)
os.makedirs('Icons/ico', exist_ok=True)

bg_tile = Image.open('tahoeappbg.png').convert('RGBA')
tile_w, tile_h = bg_tile.size # 256, 256

def create_glyph_canvas():
    return Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))

def apply_glow_and_composite(glyph_img, intensity=1.0):
    shadow = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))
    alpha = glyph_img.split()[-1]
    shadow_mask = alpha.point(lambda p: int(p * 0.45 * intensity))
    shadow_img = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 255))
    shadow.paste(shadow_img, (0, 4), shadow_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
    
    result = bg_tile.copy()
    result.alpha_composite(shadow)
    result.alpha_composite(glyph_img)
    return result

def save_icon(name, composite_img):
    png_path = f'Icons/png/{name}.png'
    ico_path = f'Icons/ico/{name}.ico'
    composite_img.save(png_path, format='PNG')
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    composite_img.save(ico_path, format='ICO', sizes=sizes)
    print(f'Generated folder icon: {name}')

# 1. Closed Folder
def gen_folder_closed():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    dark_blue = (0, 114, 206, 255)
    light_blue = (41, 169, 255, 255)
    gold = (255, 185, 0, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=dark_blue)
    draw.rounded_rectangle([84, 104, 172, 154], radius=8, fill=gold)
    draw.rounded_rectangle([74, 112, 182, 172], radius=12, fill=light_blue)
    return apply_glow_and_composite(canvas)

# 2. Open Folder
def gen_folder_open():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    dark_blue = (0, 100, 190, 255)
    light_blue = (50, 175, 255, 255)
    white = (250, 250, 255, 255)
    draw.rounded_rectangle([80, 88, 176, 164], radius=10, fill=dark_blue)
    draw.rounded_rectangle([90, 98, 166, 142], radius=4, fill=white)
    # Open front flap
    points = [(70, 174), (84, 120), (188, 120), (174, 174)]
    draw.polygon(points, fill=light_blue)
    return apply_glow_and_composite(canvas)

# 3. Documents
def gen_documents():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 120, 215, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=blue)
    # Document sheet
    draw.rounded_rectangle([96, 78, 160, 156], radius=6, fill=white)
    # Lines
    gray = (180, 190, 210, 255)
    for y in [100, 114, 128, 142]:
        draw.line([106, y, 150, y], fill=gray, width=4)
    return apply_glow_and_composite(canvas)

# 4. Downloads
def gen_downloads():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 140, 230, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=blue)
    # Down arrow
    draw.rectangle([120, 96, 136, 134], fill=white)
    draw.polygon([(110, 134), (146, 134), (128, 152)], fill=white)
    draw.rectangle([106, 156, 150, 162], fill=white)
    return apply_glow_and_composite(canvas)

# 5. Pictures
def gen_pictures():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 130, 220, 255)
    gold = (255, 185, 0, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=blue)
    # Picture frame
    draw.rounded_rectangle([92, 90, 164, 146], radius=6, fill=(245, 250, 255, 255))
    # Sun & mountains
    draw.ellipse([102, 98, 114, 110], fill=gold)
    draw.polygon([(96, 142), (116, 118), (134, 142)], fill=(40, 170, 90, 255))
    draw.polygon([(122, 142), (142, 112), (160, 142)], fill=(20, 140, 70, 255))
    return apply_glow_and_composite(canvas)

# 6. Music
def gen_music():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    pink = (235, 40, 110, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=pink)
    # Musical note
    draw.ellipse([102, 136, 120, 152], fill=white)
    draw.ellipse([136, 128, 154, 144], fill=white)
    draw.line([118, 142, 118, 102], fill=white, width=6)
    draw.line([152, 134, 152, 94], fill=white, width=6)
    draw.line([118, 102, 152, 94], fill=white, width=8)
    return apply_glow_and_composite(canvas)

# 7. Videos
def gen_videos():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    purple = (140, 50, 220, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([78, 92, 178, 166], radius=12, fill=purple)
    # Film clapper / play triangle
    draw.polygon([(116, 112), (148, 130), (116, 148)], fill=white)
    return apply_glow_and_composite(canvas)

folder_icons = {
    'folder_closed': gen_folder_closed(),
    'folder_open': gen_folder_open(),
    'documents': gen_documents(),
    'downloads': gen_downloads(),
    'pictures': gen_pictures(),
    'music': gen_music(),
    'videos': gen_videos(),
}

for name, img in folder_icons.items():
    save_icon(name, img)

print("Generated all File Explorer liquid glass folder icons!")
