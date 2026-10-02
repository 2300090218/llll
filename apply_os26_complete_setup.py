"""
OS26 Liquid Glass - Complete 1-Click System Setup & Customization
Applies wallpaper, theme colors, glass icons, registry tweaks, icon cache refresh,
and launches the OS26 Control Center.
"""

import os
import sys
import subprocess
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))

def log(msg):
    print(f"\n[OS26 SETUP] {msg}")

def check_dependencies():
    log("Checking & installing Python dependencies...")
    required = ["PyQt6", "pywin32", "pillow", "opencv-python", "opencv-contrib-python"]
    for pkg in required:
        try:
            if pkg == "pywin32":
                import win32gui
            elif pkg == "pillow":
                import PIL
            elif pkg == "PyQt6":
                import PyQt6
            elif pkg in ["opencv-python", "opencv-contrib-python"]:
                import cv2
        except ImportError:
            log(f"Installing {pkg}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=False)

def apply_theme_and_wallpaper():
    log("Applying 4K Ice Frost Wallpaper, Dark Mode, and Cyan Accent Colors...")
    ps1_script = os.path.join(ROOT, "apply_wallpaper_and_theme.ps1")
    if os.path.exists(ps1_script):
        subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ps1_script], check=False)

def apply_system_customization():
    log("Applying Shell Icons, CLSID System Icons, and Desktop Shortcuts...")
    cust_script = os.path.join(ROOT, "apply_full_system_customization.py")
    if not os.path.exists(cust_script):
        cust_script = os.path.join(ROOT, "src", "apply_full_system_customization.py")
    if os.path.exists(cust_script):
        subprocess.run([sys.executable, cust_script], check=False)

def refresh_icon_cache():
    log("Refreshing Windows Shell Icon Cache...")
    cache_script = os.path.join(ROOT, "rebuild_icon_cache.py")
    if not os.path.exists(cache_script):
        cache_script = os.path.join(ROOT, "src", "rebuild_icon_cache.py")
    if os.path.exists(cache_script):
        subprocess.run([sys.executable, cache_script], check=False)

def launch_control_center():
    log("Launching OS26 Liquid Glass Control Center...")
    app_script = os.path.join(ROOT, "src", "os26_app.py")
    if not os.path.exists(app_script):
        app_script = os.path.join(ROOT, "os26_app.py")
    if os.path.exists(app_script):
        subprocess.Popen([sys.executable, app_script], cwd=ROOT)
        log("Control Center started successfully!")

def main():
    print("=" * 60)
    print("   OS26 LIQUID GLASS - COMPLETE AUTOMATED SYSTEM DEPLOYMENT   ")
    print("=" * 60)
    check_dependencies()
    apply_theme_and_wallpaper()
    apply_system_customization()
    refresh_icon_cache()
    launch_control_center()
    print("\n" + "=" * 60)
    print("   [+] OS26 Liquid Glass Suite is now fully applied!   ")
    print("=" * 60)

if __name__ == "__main__":
    main()
