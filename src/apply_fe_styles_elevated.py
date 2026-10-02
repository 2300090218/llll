import os
import sys
import time
import yaml
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Not admin, requesting elevation...")
    script_path = os.path.abspath(__file__)
    # Re-launch elevated
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
    sys.exit(0)

print("[+] Running as Administrator!")

yaml_path = r'c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs\File_Explorer_OS26_LiquidGlass.yaml'
with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

mod_key_path = r'Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler'
settings_key_path = rf'{mod_key_path}\Settings'

# Open or create settings key
settings_key = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, settings_key_path)

# 1. Clear old values
try:
    while True:
        val_name = winreg.EnumValue(settings_key, 0)[0]
        winreg.DeleteValue(settings_key, val_name)
except OSError:
    pass

# 2. Write styleConstants
style_consts = data.get('styleConstants', [])
if isinstance(style_consts, list):
    for idx, sc in enumerate(style_consts):
        winreg.SetValueEx(settings_key, f'styleConstants[{idx}]', 0, winreg.REG_SZ, str(sc))

# 3. Write controlStyles
control_styles = data.get('controlStyles', [])
if isinstance(control_styles, list):
    for idx, cs in enumerate(control_styles):
        target = cs.get('target', '')
        winreg.SetValueEx(settings_key, f'controlStyles[{idx}].target', 0, winreg.REG_SZ, str(target))
        styles = cs.get('styles', [])
        for s_idx, st in enumerate(styles):
            winreg.SetValueEx(settings_key, f'controlStyles[{idx}].styles[{s_idx}]', 0, winreg.REG_SZ, str(st))

# 4. Other fields
winreg.SetValueEx(settings_key, 'explorerFrameContainerHeight', 0, winreg.REG_DWORD, int(data.get('explorerFrameContainerHeight', 0)))
winreg.SetValueEx(settings_key, 'xamlDiagnosticsHandling', 0, winreg.REG_SZ, str(data.get('xamlDiagnosticsHandling', '')))
winreg.SetValueEx(settings_key, 'themeResourceVariables[0]', 0, winreg.REG_SZ, '')

# 5. Background Translucent Effect for Transparent File Manager & Panels
bg_effect = data.get('backgroundTranslucentEffect', 'acrylicblur')
if bg_effect:
    winreg.SetValueEx(settings_key, 'backgroundTranslucentEffect', 0, winreg.REG_SZ, str(bg_effect))

bg_region = data.get('backgroundTranslucentEffectRegion', '')
winreg.SetValueEx(settings_key, 'backgroundTranslucentEffectRegion', 0, winreg.REG_SZ, str(bg_region))

winreg.CloseKey(settings_key)
print("[+] Successfully wrote all File Explorer styler settings to HKLM!")

# 5. Signal SettingsChangeTime to trigger Windhawk engine reload
mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, mod_key_path, 0, winreg.KEY_SET_VALUE)
now = int(time.time())
winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, now)
winreg.CloseKey(mod_key)
print(f"[+] Updated SettingsChangeTime to {now} - Windhawk will reload File Explorer styles instantly!")
