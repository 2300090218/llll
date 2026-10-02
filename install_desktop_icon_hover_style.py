import os
import sys
import time
import json
import random
import urllib.request
import winreg
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\desktop_hover_log.txt"
log = []

def write_log():
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
    except:
        pass

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    sys.exit(0)

log.append("[+] Running with Administrator privileges for Desktop Hover Style...")
write_log()

# -------------------------------------------------------------
# 1. DOWNLOAD & INSTALL DESKTOP ICON SELECTION STYLE MOD
# -------------------------------------------------------------
engine_mods_64 = r"C:\ProgramData\Windhawk\Engine\Mods\64"
os.makedirs(engine_mods_64, exist_ok=True)
now = int(time.time())

mod_id = "desktop-icon-selection-style"
mod_ver = "1.0.0"
rand_num = random.randint(100000, 999999)
dll_name = f"{mod_id}_{mod_ver}_{rand_num}.dll"
dll_path = os.path.join(engine_mods_64, dll_name)
dll_url = f"https://mods.windhawk.net/mods/{mod_id}/{mod_ver}_64.dll"

log.append(f"[*] Downloading {mod_id} from {dll_url}...")
write_log()

try:
    req = urllib.request.Request(dll_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        with open(dll_path, 'wb') as f:
            f.write(resp.read())
    log.append(f"[+] Saved {dll_name} ({os.path.getsize(dll_path)} bytes)")
except Exception as e:
    log.append(f"[-] Download failed: {e}")
    write_log()
    sys.exit(1)

# Register mod in HKLM
try:
    mod_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{mod_id}")
    winreg.SetValueEx(mod_key, "LibraryFileName", 0, winreg.REG_SZ, dll_name)
    winreg.SetValueEx(mod_key, "Disabled", 0, winreg.REG_DWORD, 0)
    winreg.SetValueEx(mod_key, "Include", 0, winreg.REG_SZ, "explorer.exe")
    winreg.SetValueEx(mod_key, "Exclude", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(mod_key, "Architecture", 0, winreg.REG_SZ, "x86-64")
    winreg.SetValueEx(mod_key, "Version", 0, winreg.REG_SZ, mod_ver)
    winreg.SetValueEx(mod_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(mod_key)
    log.append(f"[+] Registered {mod_id} in HKLM")
except Exception as e:
    log.append(f"[-] Error registering mod: {e}")

# Settings for Desktop Hover Highlight & Glow
# Rounded corners, glowing halo, bright white border on hover
settings_to_apply = {
    "widthPercent": (85, winreg.REG_DWORD),
    "topInset": (0, winreg.REG_DWORD),
    "bottomInset": (0, winreg.REG_DWORD),
    "cornerRadius": (14, winreg.REG_DWORD),
    "shape": ("auto", winreg.REG_SZ),
    "squareSize": (75, winreg.REG_DWORD),
    "fillColor": ("#FFFFFF", winreg.REG_SZ),
    "fillOpacity": (35, winreg.REG_DWORD),
    "glow": (1, winreg.REG_DWORD),
    "glowColor": ("#FFFFFF", winreg.REG_SZ),
    "glowOpacity": (50, winreg.REG_DWORD),
    "glowSize": (6, winreg.REG_DWORD),
    "glowOffsetY": (0, winreg.REG_DWORD),
    "borderStyle": ("solid", winreg.REG_SZ),
    "borderOnSelectionOnly": (0, winreg.REG_DWORD), # 0 = Show glowing border on HOVER too!
    "borderColor": ("#FFFFFF", winreg.REG_SZ),
    "borderOpacity": (85, winreg.REG_DWORD),
    "borderThickness": (2, winreg.REG_DWORD),
    "dashLength": (2, winreg.REG_DWORD),
    "dashGap": (2, winreg.REG_DWORD),
    "styleHover": (1, winreg.REG_DWORD), # 1 = Style hover plate!
    "hoverOpacity": (45, winreg.REG_DWORD),
}

try:
    cfg_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{mod_id}\Settings")
    for k, (val, reg_type) in settings_to_apply.items():
        winreg.SetValueEx(cfg_key, k, 0, reg_type, val)
    winreg.CloseKey(cfg_key)
    log.append("[+] Applied Desktop Icon Hover Highlight settings (Glow halo, rounded glass plate, solid white border on hover)")
except Exception as e:
    log.append(f"[-] Error saving desktop icon style settings: {e}")

# Update userprofile.json
profile_path = r"C:\ProgramData\Windhawk\userprofile.json"
try:
    with open(profile_path, 'r', encoding='utf-8') as f:
        u_profile = json.load(f)
    if 'mods' not in u_profile:
        u_profile['mods'] = {}
    u_profile['mods'][mod_id] = {"version": mod_ver, "latestVersion": mod_ver}
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(u_profile, f, indent=2)
    log.append("[+] Updated userprofile.json with desktop-icon-selection-style")
except Exception as e:
    log.append(f"[-] Error updating userprofile.json: {e}")

# -------------------------------------------------------------
# 2. RESTART EXPLORER TO APPLY
# -------------------------------------------------------------
log.append("[*] Restarting Windows Explorer...")
write_log()

try:
    subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
    time.sleep(2)
    subprocess.Popen(["explorer.exe"])
    time.sleep(2)
    log.append("[+] Windows Explorer restarted successfully!")
except Exception as e:
    log.append(f"[-] Error restarting Explorer: {e}")

log.append("[+] DESKTOP ICON HOVER HIGHLIGHT & GLOW SUCCESSFULLY APPLIED!")
write_log()
print("\n".join(log))
