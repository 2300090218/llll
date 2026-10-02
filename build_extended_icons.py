import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('Icons/png', exist_ok=True)
os.makedirs('Icons/ico', exist_ok=True)

bg_tile = Image.open('tahoeappbg.png').convert('RGBA')
tile_w, tile_h = bg_tile.size

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

# WhatsApp
def gen_whatsapp():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    green = (37, 211, 102, 255)
    white = (255, 255, 255, 255)
    draw.ellipse([82, 82, 174, 174], fill=green)
    # Phone handset
    draw.arc([104, 104, 146, 150], start=100, end=300, fill=white, width=12)
    draw.ellipse([102, 134, 118, 152], fill=white)
    draw.ellipse([136, 102, 152, 120], fill=white)
    return apply_glow_and_composite(canvas)

# Telegram
def gen_telegram():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (42, 171, 238, 255)
    white = (255, 255, 255, 255)
    draw.ellipse([82, 82, 174, 174], fill=blue)
    # Paper airplane
    points = [(156, 100), (96, 128), (122, 138), (142, 116), (126, 142), (144, 154)]
    draw.polygon(points, fill=white)
    return apply_glow_and_composite(canvas)

# Steam
def gen_steam():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    dark = (23, 26, 33, 255)
    white = (255, 255, 255, 255)
    draw.ellipse([82, 82, 174, 174], fill=dark)
    # Crank wheel & arm
    draw.ellipse([124, 98, 158, 132], outline=white, width=7)
    draw.line([110, 142, 132, 124], fill=white, width=12)
    draw.ellipse([98, 134, 122, 158], fill=white)
    return apply_glow_and_composite(canvas)

# Spotify
def gen_spotify():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    green = (30, 215, 96, 255)
    black = (25, 20, 20, 255)
    draw.ellipse([82, 82, 174, 174], fill=green)
    # 3 sound waves
    draw.arc([98, 102, 158, 136], start=205, end=335, fill=black, width=8)
    draw.arc([102, 118, 154, 148], start=205, end=335, fill=black, width=7)
    draw.arc([106, 134, 150, 160], start=205, end=335, fill=black, width=6)
    return apply_glow_and_composite(canvas)

# Edge
def gen_edge():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    c = (128, 128)
    # Swirl blue & green
    draw.arc([84, 84, 172, 172], start=180, end=90, fill=(0, 120, 215, 255), width=24)
    draw.arc([84, 84, 172, 172], start=90, end=0, fill=(0, 200, 140, 255), width=24)
    draw.arc([100, 100, 156, 156], start=0, end=180, fill=(0, 160, 230, 255), width=18)
    return apply_glow_and_composite(canvas)

# VS Code
def gen_vscode():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 122, 204, 255)
    light_blue = (60, 153, 220, 255)
    # Ribbon
    points1 = [(156, 86), (114, 118), (96, 106), (96, 150), (114, 138), (156, 170)]
    draw.polygon(points1, fill=blue)
    points2 = [(156, 86), (156, 170), (134, 154), (134, 102)]
    draw.polygon(points2, fill=light_blue)
    return apply_glow_and_composite(canvas)

# Recycle Bin
def gen_recycle():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 140, 240, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([92, 104, 164, 168], radius=8, fill=blue)
    draw.rounded_rectangle([86, 92, 170, 104], radius=4, fill=blue)
    # Recycle arrows
    draw.line([114, 118, 142, 118], fill=white, width=5)
    draw.line([142, 118, 134, 148], fill=white, width=5)
    draw.line([134, 148, 118, 140], fill=white, width=5)
    return apply_glow_and_composite(canvas)

# This PC / Computer
def gen_this_pc():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    screen_blue = (0, 120, 215, 255)
    frame_gray = (60, 70, 85, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([82, 88, 174, 150], radius=8, fill=frame_gray)
    draw.rounded_rectangle([88, 94, 168, 144], radius=4, fill=screen_blue)
    draw.rectangle([118, 150, 138, 164], fill=frame_gray)
    draw.rounded_rectangle([106, 162, 150, 168], radius=3, fill=frame_gray)
    return apply_glow_and_composite(canvas)

more_icons = {
    'whatsapp': gen_whatsapp(),
    'telegram': gen_telegram(),
    'steam': gen_steam(),
    'spotify': gen_spotify(),
    'microsoft_edge': gen_edge(),
    'visual_studio_code': gen_vscode(),
    'recycle_bin': gen_recycle(),
    'this_pc': gen_this_pc(),
}

for name, img in more_icons.items():
    save_icon(name, img)

print("Added extended icons suite!")
