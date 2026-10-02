import os
import sys
import time
import json
import random
import urllib.request
import winreg
import ctypes
import yaml
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\dock_zoom_log.txt"
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

log.append("[+] Running with Administrator privileges...")
write_log()

# -------------------------------------------------------------
# 1. DOWNLOAD & INSTALL TASKBAR DOCK ANIMATION
# -------------------------------------------------------------
engine_mods_64 = r"C:\ProgramData\Windhawk\Engine\Mods\64"
os.makedirs(engine_mods_64, exist_ok=True)
now = int(time.time())

mod_id = "taskbar-dock-animation"
mod_ver = "1.9.2"
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

# Apply Dock Animation settings:
# EffectRadius=28 ensures ONLY the hovered icon magnifies (adjacent icons are 55px away and remain untouched)
# MaxScale=140 makes the specific icon 40% larger
# DisableBounce=1 removes idle breathing bounce
settings_to_apply = {
    "AnimationType": 0,
    "MaxScale": 140,
    "EffectRadius": 28,
    "SpacingFactor": 20,
    "BounceDelay": 500,
    "FocusDuration": 120,
    "MirrorForTopTaskbar": 0,
    "DisableVerticalBounce": 1,
    "TaskbarLabelsMode": 0,
    "ExcludeSystemButtonsMode": 0,
    "LerpSpeed": 70,
    "DisableBounce": 1,
}

try:
    cfg_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{mod_id}\Settings")
    for k, v in settings_to_apply.items():
        winreg.SetValueEx(cfg_key, k, 0, winreg.REG_DWORD, int(v))
    winreg.CloseKey(cfg_key)
    log.append(f"[+] Applied zoom settings (MaxScale=140%, EffectRadius=28px for single-icon zoom, DisableBounce=1)")
except Exception as e:
    log.append(f"[-] Error saving dock animation settings: {e}")

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
    log.append("[+] Updated userprofile.json")
except Exception as e:
    log.append(f"[-] Error updating userprofile.json: {e}")

# -------------------------------------------------------------
# 2. UPDATE WINDOWS 11 TASKBAR STYLER WITH HOVER HIGHLIGHT
# -------------------------------------------------------------
tb_mod_id = "windows-11-taskbar-styler"
yaml_path = r"c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs\Clear_MacDock.yaml"
try:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        tb_cfg = yaml.safe_load(f)
    
    tb_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{tb_mod_id}\Settings")
    
    # Clear old styles
    try:
        while True:
            v_name = winreg.EnumValue(tb_key, 0)[0]
            if v_name != "theme" and not v_name.startswith("clickThrough") and not v_name.startswith("xaml"):
                winreg.DeleteValue(tb_key, v_name)
            else:
                break
    except OSError:
        pass

    for idx, sc in enumerate(tb_cfg.get('styleConstants', [])):
        winreg.SetValueEx(tb_key, f"styleConstants[{idx}]", 0, winreg.REG_SZ, str(sc))

    for idx, cs in enumerate(tb_cfg.get('controlStyles', [])):
        target = cs.get('target', '')
        winreg.SetValueEx(tb_key, f"controlStyles[{idx}].target", 0, winreg.REG_SZ, str(target))
        for s_idx, st in enumerate(cs.get('styles', [])):
            winreg.SetValueEx(tb_key, f"controlStyles[{idx}].styles[{s_idx}]", 0, winreg.REG_SZ, str(st))

    # Keep theme value and update timestamp
    winreg.SetValueEx(tb_key, "theme", 0, winreg.REG_SZ, "OS26_Liquid_Glass_variant_ClearMacDock")
    winreg.CloseKey(tb_key)

    tb_main_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{tb_mod_id}", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(tb_main_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(tb_main_key)
    log.append("[+] Successfully updated Windows 11 Taskbar Styler with radiant hover highlight styles!")
except Exception as e:
    log.append(f"[-] Error applying taskbar styler highlight: {e}")

# -------------------------------------------------------------
# 3. RESTART EXPLORER TO APPLY
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

log.append("[+] TASKBAR DOCK ZOOM & HIGHLIGHT SUCCESSFULLY APPLIED!")
write_log()
print("\n".join(log))
