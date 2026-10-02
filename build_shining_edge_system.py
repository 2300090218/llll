import os
import sys
import ctypes
from ctypes import wintypes
import win32gui, win32ui, win32con, win32com.client
from PIL import Image, ImageDraw, ImageFilter

OUTPUT_DIR = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons_Shining"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Tile Generator with Authentic Taskbar-Matching Shining Edge
def make_shining_edge_tile(w=256, h=256, radius=54):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    pad = 20
    box = [pad, pad, w - pad, h - pad]
    
    # 1. Outer ambient cyan/white luminous glow
    glow = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle(box, radius=radius, outline=(150, 220, 255, 140), width=5)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=4))
    img.alpha_composite(glow)
    
    # 2. Dark translucent frosted glass background (matches #2D101010 on taskbar)
    bg = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    bg_draw = ImageDraw.Draw(bg)
    bg_mask = Image.new('L', (w, h), 0)
    ImageDraw.Draw(bg_mask).rounded_rectangle(box, radius=radius, fill=255)
    
    for y in range(pad, h - pad):
        f = (y - pad) / (h - 2 * pad)
        r = int(24 * (1 - f) + 12 * f)
        g = int(34 * (1 - f) + 18 * f)
        b = int(48 * (1 - f) + 28 * f)
        a = int(195 * (1 - f) + 225 * f)
        bg_draw.line([(pad, y), (w - pad, y)], fill=(r, g, b, a))
    img.paste(bg, (0, 0), bg_mask)
    
    # 3. Top-half glossy specular highlight
    gloss = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    gloss_draw.rounded_rectangle([pad + 3, pad + 3, w - pad - 3, pad + int((h - 2 * pad) * 0.44)], radius=radius - 4, fill=(255, 255, 255, 34))
    gloss = gloss.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(gloss, (0, 0), bg_mask)
    
    # 4. The Shining Edge: Luminous Gradient Stroke (matches taskbar IconBorder)
    stroke_layer = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(stroke_layer).rounded_rectangle(box, radius=radius, outline=(255, 255, 255, 255), width=3)
    
    grad_edge = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    for y in range(h):
        for x in range(w):
            t = (x + y) / (w + h)
            if t < 0.35: # Top-left: intense white-cyan shine
                alpha = int(255 * (1 - t/0.35) + 180 * (t/0.35))
                grad_edge.putpixel((x, y), (240, 250, 255, alpha))
            elif t < 0.70: # Middle: ice-blue glass glow
                alpha = int(180 * (1 - (t-0.35)/0.35) + 95 * ((t-0.35)/0.35))
                grad_edge.putpixel((x, y), (185, 225, 255, alpha))
            else: # Bottom-right: subtle glassy rim
                alpha = int(95 * (1 - (t-0.70)/0.30) + 45 * ((t-0.70)/0.30))
                grad_edge.putpixel((x, y), (150, 200, 245, alpha))
                
    img.paste(grad_edge, (0, 0), stroke_layer.split()[-1])
    
    # 5. Top-left glint highlight arc
    glint = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    glint_draw = ImageDraw.Draw(glint)
    glint_draw.arc([pad + 2, pad + 2, pad + 80, pad + 80], start=180, end=270, fill=(255, 255, 255, 230), width=2)
    glint = glint.filter(ImageFilter.GaussianBlur(radius=1.2))
    img.alpha_composite(glint)
    
    return img

BASE_CUSHION = make_shining_edge_tile()

# 2. Extract Native High-Res Icon from Exe/Dll/Ico
def extract_native_icon(path, size=256):
    if not os.path.exists(path):
        return None
    
    # If already an ICO file
    if path.lower().endswith('.ico'):
        try:
            ico = Image.open(path).convert('RGBA')
            return ico.resize((size, size), Image.Resampling.LANCZOS)
        except:
            pass

    phicon = wintypes.HICON()
    piconid = wintypes.UINT()
    res = ctypes.windll.user32.PrivateExtractIconsW(path, 0, size, size, ctypes.byref(phicon), ctypes.byref(piconid), 1, 0)
    if res == 0 or not phicon.value:
        return None
    
    hdc = win32gui.GetDC(0)
    memdc = win32gui.CreateCompatibleDC(hdc)
    hbmp = win32gui.CreateCompatibleBitmap(hdc, size, size)
    win32gui.SelectObject(memdc, hbmp)
    win32gui.DrawIconEx(memdc, 0, 0, phicon.value, size, size, 0, 0, win32con.DI_NORMAL)
    
    bmpstr = win32ui.CreateBitmapFromHandle(hbmp).GetBitmapBits(True)
    img = Image.frombuffer('RGBA', (size, size), bmpstr, 'raw', 'BGRA', 0, 1)
    
    win32gui.DeleteDC(memdc)
    win32gui.ReleaseDC(0, hdc)
    ctypes.windll.user32.DestroyIcon(phicon)
    win32gui.DeleteObject(hbmp)
    return img

def compose_shining_icon(raw_glyph, glyph_size=138):
    if raw_glyph.size != (glyph_size, glyph_size):
        glyph = raw_glyph.resize((glyph_size, glyph_size), Image.Resampling.LANCZOS)
    else:
        glyph = raw_glyph
        
    pos = ((256 - glyph_size) // 2, (256 - glyph_size) // 2)
    
    # 3D shadow underneath glyph
    shadow = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
    alpha = glyph.split()[-1]
    shadow_mask = alpha.point(lambda p: int(p * 0.48))
    shadow_img = Image.new('RGBA', (glyph_size, glyph_size), (0, 0, 0, 255))
    shadow.paste(shadow_img, (pos[0], pos[1] + 4), shadow_mask)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=4))
    
    res = BASE_CUSHION.copy()
    res.alpha_composite(shadow)
    res.alpha_composite(glyph, pos)
    return res

def save_multi_res_ico(img, target_path):
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(target_path, format='ICO', sizes=sizes)

print("[+] Tile generator and composition ready.")
