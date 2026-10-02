import os
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

os.makedirs('Icons/png', exist_ok=True)
os.makedirs('Icons/ico', exist_ok=True)

# Load the authentic WasiXGamer OS26 tahoeappbg.png tile
bg_tile = Image.open('tahoeappbg.png').convert('RGBA')
tile_w, tile_h = bg_tile.size # 256, 256

def create_glyph_canvas():
    return Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))

def apply_glow_and_composite(glyph_img, intensity=1.0):
    # Add subtle soft shadow behind glyph
    shadow = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 0))
    alpha = glyph_img.split()[-1]
    shadow_mask = alpha.point(lambda p: int(p * 0.45 * intensity))
    shadow_img = Image.new('RGBA', (tile_w, tile_h), (0, 0, 0, 255))
    shadow.paste(shadow_img, (0, 4), shadow_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=3))
    
    # Composite: Base glass tile + shadow + glyph
    result = bg_tile.copy()
    result.alpha_composite(shadow)
    result.alpha_composite(glyph_img)
    return result

def save_icon(name, composite_img):
    png_path = f'Icons/png/{name}.png'
    ico_path = f'Icons/ico/{name}.ico'
    composite_img.save(png_path, format='PNG')
    
    # Windows standard multi-res icon
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    composite_img.save(ico_path, format='ICO', sizes=sizes)
    print(f'Generated {name}')

# 1. Windows Start / Home
def gen_start():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    # 4 cyan tiles with slight gap and tilt
    c = 128
    s = 40
    gap = 8
    # Cyan blue color like Windows 11 #00A4EF
    cyan = (0, 164, 239, 250)
    # Top-left
    draw.rounded_rectangle([c - s - gap, c - s - gap, c - gap, c - gap], radius=4, fill=cyan)
    # Top-right
    draw.rounded_rectangle([c + gap, c - s - gap, c + s + gap, c - gap], radius=4, fill=cyan)
    # Bottom-left
    draw.rounded_rectangle([c - s - gap, c + gap, c - gap, c + s + gap], radius=4, fill=cyan)
    # Bottom-right
    draw.rounded_rectangle([c + gap, c + gap, c + s + gap, c + s + gap], radius=4, fill=cyan)
    return apply_glow_and_composite(canvas)

# 2. Search / Magnifier
def gen_search():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    white = (245, 245, 250, 240)
    # circle
    draw.ellipse([92, 92, 148, 148], outline=white, width=12)
    # handle
    draw.line([138, 138, 168, 168], fill=white, width=14)
    return apply_glow_and_composite(canvas)

# 3. Task View / Window Switcher
def gen_task_view():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    white = (240, 240, 245, 230)
    # Two overlapping rounded rectangles
    draw.rounded_rectangle([88, 88, 142, 142], radius=8, outline=white, width=10)
    draw.rounded_rectangle([114, 114, 168, 168], radius=8, outline=white, width=10)
    return apply_glow_and_composite(canvas)

# 4. Google Chrome
def gen_chrome():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    # Chrome circle colors: Red, Yellow, Green, Blue center
    r = 52
    c = (128, 128)
    # Center blue
    blue = (66, 133, 244, 255)
    red = (234, 67, 53, 255)
    yellow = (251, 188, 5, 255)
    green = (52, 168, 83, 255)
    white = (255, 255, 255, 255)
    
    # Outer circle segmented
    draw.pieslice([c[0]-r, c[1]-r, c[0]+r, c[1]+r], start=-30, end=90, fill=green)
    draw.pieslice([c[0]-r, c[1]-r, c[0]+r, c[1]+r], start=90, end=210, fill=yellow)
    draw.pieslice([c[0]-r, c[1]-r, c[0]+r, c[1]+r], start=210, end=330, fill=red)
    # Inner white circle
    draw.ellipse([c[0]-28, c[1]-28, c[0]+28, c[1]+28], fill=white)
    # Center blue circle
    draw.ellipse([c[0]-22, c[1]-22, c[0]+22, c[1]+22], fill=blue)
    return apply_glow_and_composite(canvas)

# 5. File Explorer
def gen_file_explorer():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    # Folder blue & golden tab
    dark_blue = (0, 114, 206, 255)
    light_blue = (41, 169, 255, 255)
    gold = (255, 185, 0, 255)
    # Back folder flap
    draw.rounded_rectangle([80, 96, 176, 162], radius=10, fill=dark_blue)
    # Gold divider
    draw.rounded_rectangle([86, 108, 170, 150], radius=6, fill=gold)
    # Front folder flap
    draw.rounded_rectangle([76, 116, 180, 168], radius=10, fill=light_blue)
    return apply_glow_and_composite(canvas)

# 6. Microsoft Store
def gen_store():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 120, 212, 255)
    white = (255, 255, 255, 255)
    # Bag body
    draw.rounded_rectangle([82, 102, 174, 170], radius=12, fill=blue)
    # Handle
    draw.arc([106, 80, 150, 120], start=180, end=0, fill=white, width=8)
    # 4 squares on bag
    s = 12
    gap = 3
    bx, by = 128, 136
    draw.rectangle([bx - s - gap, by - s - gap, bx - gap, by - gap], fill=white)
    draw.rectangle([bx + gap, by - s - gap, bx + s + gap, by - gap], fill=white)
    draw.rectangle([bx - s - gap, by + gap, bx - gap, by + s + gap], fill=white)
    draw.rectangle([bx + gap, by + gap, bx + s + gap, by + s + gap], fill=white)
    return apply_glow_and_composite(canvas)

# 7. Discord
def gen_discord():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blurple = (88, 101, 242, 255)
    white = (255, 255, 255, 255)
    # Clyde head outline
    draw.rounded_rectangle([80, 94, 176, 162], radius=22, fill=blurple)
    # Eyes
    draw.ellipse([100, 120, 116, 136], fill=white)
    draw.ellipse([140, 120, 156, 136], fill=white)
    return apply_glow_and_composite(canvas)

# 8. Settings
def gen_settings():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    c = (128, 128)
    gray = (220, 225, 235, 250)
    # Draw gear teeth
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        dx = math.cos(rad)
        dy = math.sin(rad)
        x1 = c[0] + dx * 28 - dy * 10
        y1 = c[1] + dy * 28 + dx * 10
        x2 = c[0] + dx * 52 + dy * 10
        y2 = c[1] + dy * 52 - dx * 10
        draw.line([c[0] + dx * 28, c[1] + dy * 28, c[0] + dx * 52, c[1] + dy * 52], fill=gray, width=18)
    # Center circle
    draw.ellipse([c[0]-38, c[1]-38, c[0]+38, c[1]+38], fill=gray)
    # Center hole
    draw.ellipse([c[0]-16, c[1]-16, c[0]+16, c[1]+16], fill=(45, 55, 72, 255))
    return apply_glow_and_composite(canvas)

# 9. Terminal
def gen_terminal():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    dark = (16, 20, 28, 255)
    draw.rounded_rectangle([78, 88, 178, 168], radius=14, fill=dark)
    # > prompt
    cyan = (0, 220, 255, 255)
    draw.line([98, 116, 116, 128], fill=cyan, width=8)
    draw.line([116, 128, 98, 140], fill=cyan, width=8)
    # cursor
    draw.line([126, 142, 148, 142], fill=(240, 240, 240, 255), width=7)
    return apply_glow_and_composite(canvas)

# 10. Notepad
def gen_notepad():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 120, 215, 255)
    white = (250, 250, 255, 255)
    draw.rounded_rectangle([86, 82, 170, 174], radius=12, fill=white)
    draw.rounded_rectangle([86, 82, 170, 104], radius=8, fill=blue)
    # Note lines
    gray = (180, 190, 205, 255)
    for y in [118, 134, 150]:
        draw.line([100, y, 156, y], fill=gray, width=6)
    return apply_glow_and_composite(canvas)

# 11. Task Manager / RAM chip
def gen_task_manager():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    green = (30, 200, 100, 255)
    dark_gray = (35, 45, 55, 255)
    draw.rounded_rectangle([82, 94, 174, 162], radius=10, fill=dark_gray)
    # RAM chips on stick
    draw.rounded_rectangle([92, 108, 108, 148], radius=4, fill=green)
    draw.rounded_rectangle([114, 108, 130, 148], radius=4, fill=green)
    draw.rounded_rectangle([136, 108, 152, 148], radius=4, fill=green)
    draw.rounded_rectangle([158, 108, 164, 148], radius=2, fill=green)
    # Gold contacts at bottom
    gold = (255, 195, 0, 255)
    for x in range(86, 170, 8):
        draw.line([x, 160, x+4, 160], fill=gold, width=4)
    return apply_glow_and_composite(canvas)

# 12. GitHub
def gen_github():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    dark = (24, 28, 36, 255)
    white = (255, 255, 255, 255)
    draw.ellipse([80, 80, 176, 176], fill=dark)
    # Octocat silhouette
    draw.ellipse([98, 104, 158, 156], fill=white)
    # Ears
    draw.polygon([(100, 110), (108, 92), (120, 106)], fill=white)
    draw.polygon([(156, 110), (148, 92), (136, 106)], fill=white)
    # Eye holes
    draw.ellipse([110, 126, 122, 140], fill=dark)
    draw.ellipse([134, 126, 146, 140], fill=dark)
    return apply_glow_and_composite(canvas)

# 13. Snipping Tool
def gen_snipping_tool():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    blue = (0, 130, 230, 255)
    white = (255, 255, 255, 255)
    draw.rounded_rectangle([82, 82, 174, 174], radius=16, fill=blue)
    # Scissors
    draw.ellipse([96, 130, 118, 152], outline=white, width=6)
    draw.ellipse([138, 130, 160, 152], outline=white, width=6)
    draw.line([114, 134, 150, 96], fill=white, width=7)
    draw.line([142, 134, 106, 96], fill=white, width=7)
    return apply_glow_and_composite(canvas)

# 14. Windhawk logo
def gen_windhawk():
    canvas = create_glyph_canvas()
    draw = ImageDraw.Draw(canvas)
    white = (255, 255, 255, 255)
    # Hawk head profile
    points = [
        (92, 130), (112, 96), (142, 92), (168, 112), (150, 126),
        (164, 132), (144, 144), (160, 148), (136, 160), (112, 152),
        (98, 142)
    ]
    draw.polygon(points, fill=white)
    # Hawk eye
    draw.ellipse([126, 108, 134, 116], fill=(15, 20, 30, 255))
    return apply_glow_and_composite(canvas)

# Generate all
icons = {
    'start_menu': gen_start(),
    'search': gen_search(),
    'task_view': gen_task_view(),
    'google_chrome': gen_chrome(),
    'file_explorer': gen_file_explorer(),
    'microsoft_store': gen_store(),
    'discord': gen_discord(),
    'settings': gen_settings(),
    'terminal': gen_terminal(),
    'notepad': gen_notepad(),
    'task_manager': gen_task_manager(),
    'github': gen_github(),
    'snipping_tool': gen_snipping_tool(),
    'windhawk': gen_windhawk(),
}

for name, img in icons.items():
    save_icon(name, img)

print("Successfully generated all authentic OS26 Liquid Glass icons!")
