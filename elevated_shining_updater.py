import os
import sys
import time
import winreg
import ctypes
import pythoncom
import win32com.client

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit(0)

pythoncom.CoInitialize()
wscript = win32com.client.Dispatch('WScript.Shell')
pub_desktop = r'C:\Users\Public\Desktop'
icons_dir = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons_Shining"

mapping = {
    'Adobe Acrobat.lnk': 'adobe_acrobat.ico',
    'BlueStacks 5.lnk': 'bluestacks_5.ico',
    'BlueStacks Manager.lnk': 'bluestacks_manager.ico',
    'Microsoft Edge.lnk': 'microsoft_edge.ico',
    'MiniTool Partition Wizard.lnk': 'minitool_partition_wizard.ico',
    'MiniTool ShadowMaker.lnk': 'minitool_shadowmaker.ico',
    'Oracle VirtualBox.lnk': 'oracle_virtualbox.ico',
    'Proton VPN.lnk': 'proton_vpn.ico',
    'PyCharm 2026.1.2.lnk': 'pycharm_202612.ico',
    'VLC media player.lnk': 'vlc_media_player.ico',
    'Windhawk.lnk': 'windhawk.ico',
    'Wireshark.lnk': 'wireshark.ico',
    'Z-Library.lnk': 'z-library.ico'
}

log = []
log.append("[+] Running elevated...")
for lnk_name, ico_name in mapping.items():
    lnk_path = os.path.join(pub_desktop, lnk_name)
    ico_path = os.path.join(icons_dir, ico_name)
    if os.path.exists(lnk_path) and os.path.exists(ico_path):
        try:
            sc = wscript.CreateShortcut(lnk_path)
            sc.IconLocation = f"{ico_path},0"
            sc.Save()
            log.append(f"[+] Updated Public Desktop {lnk_name}")
        except Exception as e:
            log.append(f"[-] Error on {lnk_name}: {e}")

# Windhawk stylers shining border
SHINING_BORDER = '<LinearGradientBrush StartPoint="0.04,-0.14" EndPoint="1.22,1.10"><GradientStop Offset="0.10" Color="#90FFFFFF"/><GradientStop Offset="0.50" Color="#50A0E0FF"/><GradientStop Offset="0.95" Color="#15FFFFFF"/></LinearGradientBrush>'

# Start Menu Styler
try:
    sm_path = r'Software\Windhawk\Engine\Mods\windows-11-start-menu-styler\Settings'
    sm_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, sm_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(sm_key, 'styleConstants[8]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.SetValueEx(sm_key, 'styleConstants[9]', 0, winreg.REG_SZ, f'ElementBorderBrush={SHINING_BORDER}')
    winreg.CloseKey(sm_key)
    
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-start-menu-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] Start Menu Styler updated!")
except Exception as e:
    log.append(f"[-] Start Menu Styler error: {e}")

# File Explorer Styler
try:
    fe_path = r'Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler\Settings'
    fe_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, fe_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(fe_key, 'styleConstants[2]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.SetValueEx(fe_key, 'styleConstants[3]', 0, winreg.REG_SZ, f'ElementBorderBrush={SHINING_BORDER}')
    winreg.CloseKey(fe_key)
    
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] File Explorer Styler updated!")
except Exception as e:
    log.append(f"[-] File Explorer Styler error: {e}")

# Settings Styler
try:
    set_path = r'Software\Windhawk\Engine\Mods\windows-11-settings-styler\Settings'
    set_key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, set_path, 0, winreg.KEY_SET_VALUE | winreg.KEY_READ)
    winreg.SetValueEx(set_key, 'styleConstants[2]', 0, winreg.REG_SZ, f'BorderBrush={SHINING_BORDER}')
    winreg.CloseKey(set_key)
    
    mod_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'Software\Windhawk\Engine\Mods\windows-11-settings-styler', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(mod_key, 'SettingsChangeTime', 0, winreg.REG_DWORD, int(time.time()))
    winreg.CloseKey(mod_key)
    log.append("[+] Settings Styler updated!")
except Exception as e:
    log.append(f"[-] Settings Styler error: {e}")

with open(r"c:\Users\bhara\OneDrive\Documents\llll\elevated_shining_updater_log.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(log))
print("\n".join(log))
