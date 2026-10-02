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

if not is_admin():
    print("[*] Requesting elevation...")
    script_path = os.path.abspath(__file__)
    py_exe = sys.executable
    ctypes.windll.shell32.ShellExecuteW(None, "runas", py_exe, f'"{script_path}"', None, 1)
    sys.exit(0)

print("[+] Running as Administrator! Proceeding with automatic installation...")

engine_mods_64 = r"C:\ProgramData\Windhawk\Engine\Mods\64"
os.makedirs(engine_mods_64, exist_ok=True)
now = int(time.time())

# -------------------------------------------------------------
# 1. DOWNLOAD & INSTALL WINDOWS 11 SETTINGS STYLER
# -------------------------------------------------------------
settings_mod_id = "windows-11-settings-styler"
settings_ver = "1.1"
rand_num = random.randint(100000, 999999)
settings_dll_name = f"{settings_mod_id}_{settings_ver}_{rand_num}.dll"
settings_dll_path = os.path.join(engine_mods_64, settings_dll_name)

settings_url = f"https://mods.windhawk.net/mods/{settings_mod_id}/{settings_ver}_64.dll"
print(f"[*] Downloading {settings_mod_id} from {settings_url}...")
try:
    req = urllib.request.Request(settings_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        with open(settings_dll_path, 'wb') as f:
            f.write(resp.read())
    print(f"[+] Saved {settings_dll_name} ({os.path.getsize(settings_dll_path)} bytes)")

    # Register in HKLM
    mod_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{settings_mod_id}")
    winreg.SetValueEx(mod_key, "LibraryFileName", 0, winreg.REG_SZ, settings_dll_name)
    winreg.SetValueEx(mod_key, "Disabled", 0, winreg.REG_DWORD, 0)
    winreg.SetValueEx(mod_key, "Include", 0, winreg.REG_SZ, "SystemSettings.exe")
    winreg.SetValueEx(mod_key, "Exclude", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(mod_key, "Architecture", 0, winreg.REG_SZ, "x86-64")
    winreg.SetValueEx(mod_key, "Version", 0, winreg.REG_SZ, settings_ver)
    winreg.SetValueEx(mod_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(mod_key)

    # Apply Translucent/WindowGlass settings into Settings subkey
    settings_cfg_path = r"c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs\Settings_Translucent11.yaml"
    if os.path.exists(settings_cfg_path):
        with open(settings_cfg_path, 'r', encoding='utf-8') as f:
            cfg = yaml.safe_load(f)
        
        cfg_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{settings_mod_id}\Settings")
        # styleConstants
        for idx, sc in enumerate(cfg.get('styleConstants', [])):
            winreg.SetValueEx(cfg_key, f"styleConstants[{idx}]", 0, winreg.REG_SZ, str(sc))
        # controlStyles
        for idx, cs in enumerate(cfg.get('controlStyles', [])):
            target = cs.get('target', '')
            winreg.SetValueEx(cfg_key, f"controlStyles[{idx}].target", 0, winreg.REG_SZ, str(target))
            for s_idx, st in enumerate(cs.get('styles', [])):
                winreg.SetValueEx(cfg_key, f"controlStyles[{idx}].styles[{s_idx}]", 0, winreg.REG_SZ, str(st))
        winreg.SetValueEx(cfg_key, "theme", 0, winreg.REG_SZ, "Translucent_Settings11")
        winreg.CloseKey(cfg_key)
        print("[+] Applied Translucent Settings styling into registry!")

except Exception as e:
    print(f"[-] Error installing Settings Styler: {e}")

# -------------------------------------------------------------
# 2. DOWNLOAD & INSTALL NOTIFICATION CENTER STYLER (Control Pane)
# -------------------------------------------------------------
nc_mod_id = "windows-11-notification-center-styler"
nc_ver = "1.7"
rand_num2 = random.randint(100000, 999999)
nc_dll_name = f"{nc_mod_id}_{nc_ver}_{rand_num2}.dll"
nc_dll_path = os.path.join(engine_mods_64, nc_dll_name)

nc_url = f"https://mods.windhawk.net/mods/{nc_mod_id}/{nc_ver}_64.dll"
print(f"[*] Downloading {nc_mod_id} from {nc_url}...")
try:
    req = urllib.request.Request(nc_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        with open(nc_dll_path, 'wb') as f:
            f.write(resp.read())
    print(f"[+] Saved {nc_dll_name} ({os.path.getsize(nc_dll_path)} bytes)")

    # Register in HKLM
    mod_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{nc_mod_id}")
    winreg.SetValueEx(mod_key, "LibraryFileName", 0, winreg.REG_SZ, nc_dll_name)
    winreg.SetValueEx(mod_key, "Disabled", 0, winreg.REG_DWORD, 0)
    winreg.SetValueEx(mod_key, "Include", 0, winreg.REG_SZ, "ShellExperienceHost.exe")
    winreg.SetValueEx(mod_key, "Exclude", 0, winreg.REG_SZ, "")
    winreg.SetValueEx(mod_key, "Architecture", 0, winreg.REG_SZ, "x86-64")
    winreg.SetValueEx(mod_key, "Version", 0, winreg.REG_SZ, nc_ver)
    winreg.SetValueEx(mod_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(mod_key)

    # Set TranslucentShell theme
    cfg_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{nc_mod_id}\Settings")
    winreg.SetValueEx(cfg_key, "theme", 0, winreg.REG_SZ, "TranslucentShell")
    winreg.CloseKey(cfg_key)
    print("[+] Applied TranslucentShell theme to Notification/Control Center!")

except Exception as e:
    print(f"[-] Error installing Notification Center Styler: {e}")

# -------------------------------------------------------------
# 3. UPDATE FILE EXPLORER STYLER SETTINGS
# -------------------------------------------------------------
fe_mod_id = "windows-11-file-explorer-styler"
fe_cfg_path = r"c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs\File_Explorer_OS26_LiquidGlass.yaml"
try:
    with open(fe_cfg_path, 'r', encoding='utf-8') as f:
        fe_cfg = yaml.safe_load(f)
    
    fe_settings_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{fe_mod_id}\Settings")
    # Clear old values
    try:
        while True:
            v_name = winreg.EnumValue(fe_settings_key, 0)[0]
            winreg.DeleteValue(fe_settings_key, v_name)
    except OSError:
        pass

    for idx, sc in enumerate(fe_cfg.get('styleConstants', [])):
        winreg.SetValueEx(fe_settings_key, f"styleConstants[{idx}]", 0, winreg.REG_SZ, str(sc))

    for idx, cs in enumerate(fe_cfg.get('controlStyles', [])):
        target = cs.get('target', '')
        winreg.SetValueEx(fe_settings_key, f"controlStyles[{idx}].target", 0, winreg.REG_SZ, str(target))
        for s_idx, st in enumerate(cs.get('styles', [])):
            winreg.SetValueEx(fe_settings_key, f"controlStyles[{idx}].styles[{s_idx}]", 0, winreg.REG_SZ, str(st))

    winreg.SetValueEx(fe_settings_key, "explorerFrameContainerHeight", 0, winreg.REG_DWORD, int(fe_cfg.get('explorerFrameContainerHeight', 0)))
    winreg.SetValueEx(fe_settings_key, "xamlDiagnosticsHandling", 0, winreg.REG_SZ, str(fe_cfg.get('xamlDiagnosticsHandling', '')))
    winreg.SetValueEx(fe_settings_key, "themeResourceVariables[0]", 0, winreg.REG_SZ, "")

    bg_effect = fe_cfg.get('backgroundTranslucentEffect', 'acrylicblur')
    if bg_effect:
        winreg.SetValueEx(fe_settings_key, "backgroundTranslucentEffect", 0, winreg.REG_SZ, str(bg_effect))
    bg_region = fe_cfg.get('backgroundTranslucentEffectRegion', '')
    winreg.SetValueEx(fe_settings_key, "backgroundTranslucentEffectRegion", 0, winreg.REG_SZ, str(bg_region))

    winreg.CloseKey(fe_settings_key)

    fe_mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, rf"Software\Windhawk\Engine\Mods\{fe_mod_id}", 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(fe_mod_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
    winreg.CloseKey(fe_mod_key)
    print("[+] Successfully updated File Explorer frosted glass settings!")

except Exception as e:
    print(f"[-] Error updating File Explorer Styler: {e}")

# -------------------------------------------------------------
# 4. UPDATE USERPROFILE.JSON
# -------------------------------------------------------------
profile_path = r"C:\ProgramData\Windhawk\userprofile.json"
try:
    with open(profile_path, 'r', encoding='utf-8') as f:
        u_profile = json.load(f)
    if 'mods' not in u_profile:
        u_profile['mods'] = {}
    u_profile['mods'][settings_mod_id] = {"version": settings_ver, "latestVersion": settings_ver}
    u_profile['mods'][nc_mod_id] = {"version": nc_ver, "latestVersion": nc_ver}
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(u_profile, f, indent=2)
    print("[+] Updated userprofile.json with installed mods!")
except Exception as e:
    print(f"[-] userprofile.json update error: {e}")

# -------------------------------------------------------------
# 5. RESTART TARGET PROCESSES SO STYLES APPLY IMMEDIATELY
# -------------------------------------------------------------
print("[*] Refreshing target processes...")
try:
    subprocess.run(["taskkill", "/f", "/im", "SystemSettings.exe"], capture_output=True)
    subprocess.run(["taskkill", "/f", "/im", "ShellExperienceHost.exe"], capture_output=True)
except:
    pass

print("[+] Done! All mods and styles have been installed and applied!")
