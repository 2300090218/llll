import os
import math
from PIL import Image, ImageDraw, ImageFilter

os.makedirs('Icons/png', exist_ok=True)
os.makedirs('Icons/ico', exist_ok=True)

bg_tile = Image.open('tahoeappbg.png').convert('RGBA')
tile_w, tile_h = bg_tile.size

def create_canvas():
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
    print(f"Generated {name}.ico")

# 1. VLC
def gen_vlc():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    # Traffic cone
    orange = (255, 120, 0, 255)
    white = (255, 255, 255, 255)
    d.polygon([(128, 86), (92, 160), (164, 160)], fill=orange)
    d.polygon([(128, 108), (112, 138), (144, 138)], fill=white)
    d.ellipse([84, 156, 172, 170], fill=orange)
    return apply_glow_and_composite(c)

# 2. Wireshark
def gen_wireshark():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    blue = (0, 115, 215, 255)
    white = (255, 255, 255, 255)
    # Shark fin
    d.polygon([(96, 164), (120, 92), (160, 128), (160, 164)], fill=blue)
    d.polygon([(108, 164), (122, 110), (148, 138), (148, 164)], fill=white)
    return apply_glow_and_composite(c)

# 3. Proton (VPN / Mail / Drive)
def gen_proton():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    purple = (110, 80, 240, 255)
    cyan = (100, 220, 255, 255)
    d.rounded_rectangle([92, 92, 164, 164], radius=20, fill=purple)
    d.arc([100, 100, 156, 156], start=180, end=360, fill=cyan, width=12)
    d.line([128, 110, 128, 146], fill=(255, 255, 255, 255), width=8)
    return apply_glow_and_composite(c)

# 4. BlueStacks
def gen_bluestacks():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    # 4 colored layered tiles
    d.rounded_rectangle([90, 90, 130, 130], radius=8, fill=(0, 168, 240, 255))
    d.rounded_rectangle([126, 90, 166, 130], radius=8, fill=(255, 185, 0, 255))
    d.rounded_rectangle([90, 126, 130, 166], radius=8, fill=(115, 195, 0, 255))
    d.rounded_rectangle([126, 126, 166, 166], radius=8, fill=(240, 70, 70, 255))
    return apply_glow_and_composite(c)

# 5. PyCharm
def gen_pycharm():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    # Dark square badge with green/yellow PC
    dark = (33, 33, 33, 255)
    green = (33, 215, 137, 255)
    yellow = (255, 215, 0, 255)
    d.rounded_rectangle([86, 86, 170, 170], radius=16, fill=dark)
    d.rounded_rectangle([86, 86, 170, 100], radius=8, fill=green)
    # 'PC' text approximation
    d.rectangle([102, 112, 114, 152], fill=green)
    d.arc([102, 112, 130, 134], start=270, end=90, fill=green, width=6)
    d.arc([136, 114, 154, 150], start=90, end=270, fill=yellow, width=6)
    return apply_glow_and_composite(c)

# 6. Brave
def gen_brave():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    orange = (255, 85, 0, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([88, 88, 168, 168], radius=24, fill=orange)
    # Lion face crown
    d.polygon([(102, 112), (128, 96), (154, 112), (144, 148), (112, 148)], fill=white)
    return apply_glow_and_composite(c)

# 7. Adobe Acrobat / Express
def gen_adobe():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    red = (235, 20, 20, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([86, 86, 170, 170], radius=18, fill=red)
    # A ribbon
    d.arc([98, 100, 158, 160], start=180, end=360, fill=white, width=10)
    d.line([104, 152, 152, 152], fill=white, width=8)
    return apply_glow_and_composite(c)

# 8. VirtualBox
def gen_virtualbox():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    blue = (25, 95, 215, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([86, 86, 170, 170], radius=18, fill=blue)
    # 3D Cube lines
    d.rectangle([102, 102, 154, 154], outline=white, width=5)
    d.line([102, 102, 120, 90], fill=white, width=5)
    d.line([154, 102, 170, 90], fill=white, width=5)
    d.line([120, 90, 170, 90], fill=white, width=5)
    d.line([170, 90, 170, 142], fill=white, width=5)
    d.line([154, 154, 170, 142], fill=white, width=5)
    return apply_glow_and_composite(c)

# 9. Free Download Manager
def gen_fdm():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    blue = (0, 140, 240, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([86, 86, 170, 170], radius=20, fill=blue)
    # Arrow down
    d.line([128, 104, 128, 144], fill=white, width=10)
    d.polygon([(112, 136), (128, 154), (144, 136)], fill=white)
    return apply_glow_and_composite(c)

# 10. Calculator
def gen_calculator():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    dark_gray = (50, 60, 75, 255)
    blue = (0, 150, 255, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([90, 86, 166, 170], radius=14, fill=dark_gray)
    d.rounded_rectangle([98, 96, 158, 116], radius=4, fill=blue)
    # Buttons
    for y in [124, 138, 152]:
        for x in [98, 114, 130, 146]:
            d.rectangle([x, y, x+8, y+8], fill=white)
    return apply_glow_and_composite(c)

# 11. Photos
def gen_photos():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    # 4 colorful flower petals
    d.ellipse([108, 90, 148, 130], fill=(255, 80, 80, 255))
    d.ellipse([126, 108, 166, 148], fill=(255, 180, 0, 255))
    d.ellipse([108, 126, 148, 166], fill=(0, 180, 255, 255))
    d.ellipse([90, 108, 130, 148], fill=(50, 205, 50, 255))
    return apply_glow_and_composite(c)

# 12. Paint
def gen_paint():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    white = (250, 250, 250, 255)
    d.ellipse([88, 92, 168, 164], fill=white)
    # Paint dollops
    d.ellipse([100, 112, 112, 124], fill=(255, 50, 50, 255))
    d.ellipse([120, 102, 132, 114], fill=(255, 200, 0, 255))
    d.ellipse([142, 114, 154, 126], fill=(0, 150, 255, 255))
    d.ellipse([144, 138, 156, 150], fill=(50, 200, 50, 255))
    d.ellipse([108, 142, 120, 154], fill=(180, 50, 255, 255))
    return apply_glow_and_composite(c)

# 13. Clock
def gen_clock():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    dark = (40, 50, 65, 255)
    blue = (0, 160, 255, 255)
    white = (255, 255, 255, 255)
    d.ellipse([86, 86, 170, 170], fill=dark, outline=blue, width=6)
    # Hands at 10:10
    d.line([128, 128, 108, 106], fill=white, width=6)
    d.line([128, 128, 148, 112], fill=blue, width=5)
    d.ellipse([124, 124, 132, 132], fill=white)
    return apply_glow_and_composite(c)

# 14. Outlook / Mail
def gen_outlook():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    blue = (0, 114, 198, 255)
    white = (255, 255, 255, 255)
    d.rounded_rectangle([86, 96, 170, 160], radius=12, fill=blue)
    d.polygon([(92, 100), (128, 130), (164, 100)], fill=white)
    d.arc([114, 116, 142, 144], start=0, end=360, fill=white, width=5)
    return apply_glow_and_composite(c)

# 15. Cisco / Network
def gen_cisco():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    cyan = (0, 180, 220, 255)
    white = (255, 255, 255, 255)
    d.ellipse([86, 86, 170, 170], fill=cyan)
    # Network arrows
    d.line([100, 128, 156, 128], fill=white, width=6)
    d.line([128, 100, 128, 156], fill=white, width=6)
    return apply_glow_and_composite(c)

# 16. Eclipse
def gen_eclipse():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    purple = (60, 40, 120, 255)
    orange = (245, 145, 30, 255)
    d.ellipse([86, 86, 170, 170], fill=purple)
    d.arc([94, 94, 162, 162], start=210, end=30, fill=orange, width=12)
    return apply_glow_and_composite(c)

# 17. Tor Browser
def gen_tor():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    purple = (125, 70, 150, 255)
    white = (255, 255, 255, 255)
    d.ellipse([86, 86, 170, 170], fill=purple)
    # Onion rings
    d.arc([100, 100, 156, 156], start=90, end=270, fill=white, width=6)
    d.arc([112, 112, 144, 144], start=90, end=270, fill=white, width=6)
    d.arc([122, 122, 134, 134], start=90, end=270, fill=white, width=5)
    return apply_glow_and_composite(c)

# 18. MiniTool
def gen_minitool():
    c = create_canvas()
    d = ImageDraw.Draw(c)
    blue = (0, 130, 220, 255)
    gold = (255, 200, 0, 255)
    d.rounded_rectangle([86, 86, 170, 170], radius=16, fill=blue)
    # Wizard wand / star
    d.line([100, 156, 156, 100], fill=(255, 255, 255, 255), width=7)
    d.ellipse([146, 92, 164, 110], fill=gold)
    return apply_glow_and_composite(c)

new_icons = {
    'vlc': gen_vlc(),
    'wireshark': gen_wireshark(),
    'proton': gen_proton(),
    'bluestacks': gen_bluestacks(),
    'pycharm': gen_pycharm(),
    'brave': gen_brave(),
    'adobe': gen_adobe(),
    'virtualbox': gen_virtualbox(),
    'fdm': gen_fdm(),
    'calculator': gen_calculator(),
    'photos': gen_photos(),
    'paint': gen_paint(),
    'clock': gen_clock(),
    'outlook': gen_outlook(),
    'cisco': gen_cisco(),
    'eclipse': gen_eclipse(),
    'tor': gen_tor(),
    'minitool': gen_minitool(),
}

for name, img in new_icons.items():
    save_icon(name, img)

print("Finished generating all extra app icons!")
