import os
import shutil

root = r"c:\Users\bhara\OneDrive\Documents\llll"

dirs = [
    os.path.join(root, "src"),
    os.path.join(root, "assets", "icons"),
    os.path.join(root, "assets", "wallpaper"),
    os.path.join(root, "assets", "windhawk"),
    os.path.join(root, "assets", "previews"),
    os.path.join(root, "scripts"),
    os.path.join(root, "installer"),
    os.path.join(root, "dist", "windows")
]

for d in dirs:
    os.makedirs(d, exist_ok=True)
    print("Created dir:", d)

# Copy icons
icons_src = os.path.join(root, "Icons", "ico")
if os.path.exists(icons_src):
    icons_dest = os.path.join(root, "assets", "icons")
    for f in os.listdir(icons_src):
        if f.endswith(".ico"):
            shutil.copy2(os.path.join(icons_src, f), os.path.join(icons_dest, f))
    print(f"Copied {len(os.listdir(icons_dest))} icons to assets/icons")

# Copy wallpaper
wp_src = os.path.join(root, "OS26_Ice_Frost_Wallpaper_4K.jpg")
if os.path.exists(wp_src):
    shutil.copy2(wp_src, os.path.join(root, "assets", "wallpaper", "OS26_Ice_Frost_Wallpaper_4K.jpg"))
    print("Copied wallpaper to assets/wallpaper")

# Copy Windhawk setup and configs
wh_setup = os.path.join(root, "windhawk_setup.exe")
if os.path.exists(wh_setup):
    shutil.copy2(wh_setup, os.path.join(root, "assets", "windhawk", "windhawk_setup.exe"))
    print("Copied windhawk_setup.exe to assets/windhawk")

wh_configs = os.path.join(root, "Windhawk_Configs")
if os.path.exists(wh_configs):
    wh_dest = os.path.join(root, "assets", "windhawk", "configs")
    os.makedirs(wh_dest, exist_ok=True)
    for f in os.listdir(wh_configs):
        if f.endswith(".yaml"):
            shutil.copy2(os.path.join(wh_configs, f), os.path.join(wh_dest, f))
    print(f"Copied {len(os.listdir(wh_dest))} YAML configs to assets/windhawk/configs")

# Copy preview images
previews = [
    "screenshot-dock.png",
    "screenshot-taskbar.png",
    "screenshot-dock-dark.png",
    "screenshot-taskbar-dark.png",
    "tahoeappbg.png",
    "menu.png",
    "selector.png",
    "screenshot_clean_desktop.png"
]
for p in previews:
    p_path = os.path.join(root, p)
    if os.path.exists(p_path):
        shutil.copy2(p_path, os.path.join(root, "assets", "previews", p))
        print("Copied preview:", p)

# Copy scripts
scripts = [
    "ENTER_EXAM_MODE.bat",
    "RESTORE_WINDHAWK_THEME.bat",
    "START_DESKTOP_ICON_VIBRATION.bat",
    "STOP_DESKTOP_ICON_VIBRATION.bat",
    "unthrottle_full_brightness.bat",
    "organize_desktop_project_tools.py"
]
for s in scripts:
    s_path = os.path.join(root, s)
    if os.path.exists(s_path):
        shutil.copy2(s_path, os.path.join(root, "scripts", s))
        print("Copied script:", s)

print("Project build structure initialized successfully!")
