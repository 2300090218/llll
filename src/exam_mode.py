"""
OS26 Liquid Glass: Exam Safe Mode & Theme Restoration Engine
Provides 1-click seamless switching between 100% Exam Safe Mode and Full Liquid Glass Theme.
"""

import os
import sys
import subprocess
import time
import win32com.client
import psutil

STARTUP_DIR = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
DISABLED_DIR = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup_Disabled")

TARGET_SHORTCUTS = [
    "LiquidGlassDock.lnk",
    "MacBrightnessEngine.lnk",
    "DesktopIconVibration.lnk"
]

def is_exam_mode_active():
    """Returns True if exam mode is active (Windhawk stopped, startup shortcuts disabled)."""
    # Check if disabled dir has shortcuts
    if os.path.exists(DISABLED_DIR) and len(os.listdir(DISABLED_DIR)) > 0:
        return True
    # Check if any windhawk process is running
    for proc in psutil.process_iter(['name']):
        try:
            if "windhawk" in proc.info['name'].lower():
                return False
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def enter_exam_mode():
    """
    Terminates Windhawk and background customization daemons.
    Disables startup shortcuts.
    Flushes Windows Explorer memory.
    Keeps permanent custom icons, wallpaper, and native theme 100% intact.
    """
    os.makedirs(DISABLED_DIR, exist_ok=True)

    # 1. Stop background Python processes
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            cmdline = " ".join(proc.info['cmdline'] or []).lower()
            if any(k in cmdline for k in ["desktop_zoom_dock.py", "mac_brightness_engine.py", "desktop_icon_vibrator.py"]):
                proc.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # 2. Disable startup shortcuts
    for sc in TARGET_SHORTCUTS:
        src = os.path.join(STARTUP_DIR, sc)
        dst = os.path.join(DISABLED_DIR, sc)
        if os.path.exists(src):
            try:
                os.replace(src, dst)
            except Exception:
                pass

    # 3. Stop Windhawk service and processes
    subprocess.run(["sc", "config", "Windhawk", "start=", "demand"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["net", "stop", "Windhawk"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for proc in psutil.process_iter(['name']):
        try:
            if "windhawk" in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    # 4. Restart Explorer cleanly
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"])
    return True

def restore_full_theme(workspace_root=None):
    """
    Restores Windhawk service, startup shortcuts, and launches background engines.
    """
    # 1. Restore startup shortcuts
    if os.path.exists(DISABLED_DIR):
        for sc in TARGET_SHORTCUTS:
            src = os.path.join(DISABLED_DIR, sc)
            dst = os.path.join(STARTUP_DIR, sc)
            if os.path.exists(src):
                try:
                    os.replace(src, dst)
                except Exception:
                    pass

    # 2. Start Windhawk service
    subprocess.run(["sc", "config", "Windhawk", "start=", "auto"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["net", "start", "Windhawk"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Launch Windhawk UI in tray
    wh_exe = r"C:\Program Files\Windhawk\windhawk.exe"
    if os.path.exists(wh_exe):
        subprocess.Popen([wh_exe, "-tray"])

    # 4. Restart Explorer to attach hooks
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.Popen(["explorer.exe"])

    # 5. Launch background daemons
    if workspace_root:
        pyw = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
        if os.path.exists(pyw):
            dock_script = os.path.join(workspace_root, "desktop_zoom_dock.py")
            if os.path.exists(dock_script):
                subprocess.Popen([pyw, dock_script], cwd=workspace_root)
            vibe_script = os.path.join(workspace_root, "desktop_icon_vibrator.py")
            if os.path.exists(vibe_script):
                subprocess.Popen([pyw, vibe_script], cwd=workspace_root)
    return True
