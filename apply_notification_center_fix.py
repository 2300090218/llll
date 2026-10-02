import os
import sys
import time
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
    print("[*] Requesting elevation for Win+A fix...")
    script_path = os.path.abspath(__file__)
    py_exe = sys.executable
    ctypes.windll.shell32.ShellExecuteW(None, "runas", py_exe, f'"{script_path}"', None, 1)
    sys.exit(0)

print("[+] Running elevated! Configuring Windows 11 Notification Center & Quick Settings (Win+A)...")

nc_mod_id = "windows-11-notification-center-styler"
mod_key_path = rf"Software\Windhawk\Engine\Mods\{nc_mod_id}"
settings_key_path = rf"{mod_key_path}\Settings"
now = int(time.time())

# 1. Update Include list to cover BOTH ShellExperienceHost.exe and ShellHost.exe
mod_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, mod_key_path)
winreg.SetValueEx(mod_key, "Include", 0, winreg.REG_SZ, "ShellExperienceHost.exe|ShellHost.exe")
winreg.SetValueEx(mod_key, "Disabled", 0, winreg.REG_DWORD, 0)
winreg.SetValueEx(mod_key, "Architecture", 0, winreg.REG_SZ, "x86-64")
winreg.SetValueEx(mod_key, "Version", 0, winreg.REG_SZ, "1.7")
winreg.SetValueEx(mod_key, "SettingsChangeTime", 0, winreg.REG_DWORD, now)
winreg.CloseKey(mod_key)
print("[+] Set Include = 'ShellExperienceHost.exe|ShellHost.exe'")

# 2. Read and customize TranslucentShell yaml
yaml_path = r"c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs\NotificationCenter_TranslucentShell.yaml"
with open(yaml_path, 'r', encoding='utf-8') as f:
    cfg = yaml.safe_load(f)

# Use matching Start Menu frosted acrylic blur
cfg['styleConstants'] = [
    'CommonBgBrush=<WindhawkBlur BlurAmount="20" TintColor="{ThemeResource SystemAltLowColor}" TintOpacity="0.25" />',
    'thumbnailImageSize=240'
]

# Write to registry
settings_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, settings_key_path)

# Clear old values
try:
    while True:
        v_name = winreg.EnumValue(settings_key, 0)[0]
        winreg.DeleteValue(settings_key, v_name)
except OSError:
    pass

# styleConstants
for idx, sc in enumerate(cfg.get('styleConstants', [])):
    winreg.SetValueEx(settings_key, f"styleConstants[{idx}]", 0, winreg.REG_SZ, str(sc))

# controlStyles
for idx, cs in enumerate(cfg.get('controlStyles', [])):
    target = cs.get('target', '')
    winreg.SetValueEx(settings_key, f"controlStyles[{idx}].target", 0, winreg.REG_SZ, str(target))
    for s_idx, st in enumerate(cs.get('styles', [])):
        winreg.SetValueEx(settings_key, f"controlStyles[{idx}].styles[{s_idx}]", 0, winreg.REG_SZ, str(st))

winreg.SetValueEx(settings_key, "theme", 0, winreg.REG_SZ, "TranslucentShell")
winreg.CloseKey(settings_key)
print(f"[+] Wrote {len(cfg.get('controlStyles', []))} control styles to {settings_key_path}")

# 3. Kill ShellHost and ShellExperienceHost so Windows restarts them with the mod hooked
print("[*] Restarting ShellHost.exe and ShellExperienceHost.exe...")
subprocess.run(["taskkill", "/f", "/im", "ShellHost.exe"], capture_output=True)
subprocess.run(["taskkill", "/f", "/im", "ShellExperienceHost.exe"], capture_output=True)

print("[+] Done! Quick Settings (Win+A) has been updated with translucent frosted glass!")
