import os
import sys
import time
import winreg
import ctypes
import win32com.client

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit(0)

log = []
log.append("[+] Running elevated shining edge configuration...")

# 1. Update Public Desktop shortcuts
wscript = win32com.client.Dispatch('WScript.Shell')
pub_desktop = r'C:\Users\Public\Desktop'
icons_dir = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons_Shining"

if os.path.exists(pub_desktop):
    for f in os.listdir(pub_desktop):
        if not f.endswith('.lnk'): continue
        lnk_path = os.path.join(pub_desktop, f)
        base_name = os.path.splitext(f)[0]
        safe_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_').lower()
        ico_dest = os.path.join(icons_dir, f"{safe_name}.ico")
        
        # Check if icon exists or fallback to general match
        if not os.path.exists(ico_dest):
            for existing in os.listdir(icons_dir):
                if existing.endswith('.ico'):
                    k = os.path.splitext(existing)[0]
                    if k in safe_name or safe_name in k:
                        ico_dest = os.path.join(icons_dir, existing)
                        break
                        
        if os.path.exists(ico_dest):
            try:
                sc = wscript.CreateShortcut(lnk_path)
                sc.IconLocation = f"{ico_dest},0"
                sc.Save()
                log.append(f"[+] Public desktop icon updated: {f} -> {ico_dest}")
            except Exception as e:
                log.append(f"[-] Failed to update {f}: {e}")

# 2. Shining Edge Gradient Definition
SHINING_BORDER = '<LinearGradientBrush StartPoint="0.04,-0.14" EndPoint="1.22,1.10"><GradientStop Offset="0.10" Color="#90FFFFFF"/><GradientStop Offset="0.50" Color="#50A0E0FF"/><GradientStop Offset="0.95" Color="#15FFFFFF"/></LinearGradientBrush>'

# 3. Apply to Start Menu Styler
try:
    sm_path = r'Software\Windhawk\Engine\Mods\windows-11-start-menu-styler\Settings'
    sm_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, sm_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(sm_key, 'styleConstants[8]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.SetValueEx(sm_key, 'styleConstants[9]', 0, winreg.REG_SZ, f'ElementBorderBrush={SHINING_BORDER}')
    
    # Also set pinned items, list items, search box to always have shining border
    # Add new controlStyles targets if needed
    winreg.CloseKey(sm_key)
    
    # Trigger SettingsChangeTime
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-start-menu-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] Start Menu Styler updated with shining edge gradient!")
except Exception as e:
    log.append(f"[-] Start Menu Styler update error: {e}")

# 4. Apply to File Explorer Styler
try:
    fe_path = r'Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler\Settings'
    fe_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, fe_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(fe_key, 'styleConstants[2]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.SetValueEx(fe_key, 'styleConstants[3]', 0, winreg.REG_SZ, f'ElementBorderBrush={SHINING_BORDER}')
    winreg.CloseKey(fe_key)
    
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] File Explorer Styler updated with shining edge gradient!")
except Exception as e:
    log.append(f"[-] File Explorer Styler update error: {e}")

# 5. Apply to Settings Styler
try:
    set_path = r'Software\Windhawk\Engine\Mods\windows-11-settings-styler\Settings'
    set_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, set_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(set_key, 'styleConstants[2]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.CloseKey(set_key)
    
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-settings-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] Settings Styler updated with shining edge gradient!")
except Exception as e:
    log.append(f"[-] Settings Styler update error: {e}")

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\shining_edge_elevated_log.txt"
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("\n".join(log))
