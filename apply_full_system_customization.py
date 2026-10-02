import os
import sys
import shutil
import winreg
import ctypes
from ctypes import wintypes
import win32com.client

print("=======================================================")
print(" OS26 LIQUID GLASS: FULL SYSTEM CUSTOMIZATION ENGINE  ")
print("=======================================================")

user_profile = os.environ['USERPROFILE']
icons_src = r'c:\Users\bhara\OneDrive\Documents\llll\Icons\ico'
permanent_dir = r'C:\Users\bhara\AppData\Local\OS26_Liquid_Glass'
icons_dest = os.path.join(permanent_dir, 'Icons')
wallpaper_path = os.path.join(permanent_dir, 'OS26_Ice_Frost_Wallpaper_4K.jpg')

os.makedirs(icons_dest, exist_ok=True)

# 1. Copy wallpaper if needed
if os.path.exists(r'c:\Users\bhara\OneDrive\Documents\llll\OS26_Ice_Frost_Wallpaper_4K.jpg'):
    shutil.copy2(r'c:\Users\bhara\OneDrive\Documents\llll\OS26_Ice_Frost_Wallpaper_4K.jpg', wallpaper_path)

# 2. Copy all icons to permanent AppData directory
for f in os.listdir(icons_src):
    if f.endswith('.ico'):
        shutil.copy2(os.path.join(icons_src, f), os.path.join(icons_dest, f))
print(f"[+] Synced {len(os.listdir(icons_dest))} liquid glass icons to {icons_dest}")

# 3. Register Global Shell Icons in Registry
folder_closed_ico = os.path.join(icons_dest, 'folder_closed.ico')
folder_open_ico = os.path.join(icons_dest, 'folder_open.ico')

shell_icons_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons')
winreg.SetValueEx(shell_icons_key, '3', 0, winreg.REG_SZ, f'{folder_closed_ico},0')
winreg.SetValueEx(shell_icons_key, '4', 0, winreg.REG_SZ, f'{folder_open_ico},0')
winreg.SetValueEx(shell_icons_key, '162', 0, winreg.REG_SZ, f'{folder_closed_ico},0')
winreg.CloseKey(shell_icons_key)
print("[+] Registered global Shell Icons (Folder closed/open/quick access) in registry")

# 4. Register CLSID System Icons (Recycle Bin, This PC)
def set_reg_val(root, subkey, val_name, val):
    k = winreg.CreateKey(root, subkey)
    winreg.SetValueEx(k, val_name, 0, winreg.REG_SZ, val)
    winreg.CloseKey(k)

recycle_ico = os.path.join(icons_dest, 'recycle_bin.ico')
this_pc_ico = os.path.join(icons_dest, 'this_pc.ico')

set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon', '', f'{recycle_ico},0')
set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon', 'empty', f'{recycle_ico},0')
set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{645FF040-5081-101B-9F08-00AA002F954E}\DefaultIcon', 'full', f'{recycle_ico},0')

set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\CLSID\{20D04FE0-3AEA-1069-A2D8-08002B30309D}\DefaultIcon', '', f'{this_pc_ico},0')
print("[+] Registered CLSID icons for Recycle Bin & This PC")

# 5. Lock Screen / Startup screen background
try:
    set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\PersonalizationCSP', 'LockScreenImagePath', wallpaper_path)
    set_reg_val(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\PersonalizationCSP', 'LockScreenImageUrl', wallpaper_path)
    print("[+] Registered OS26 Ice Frost wallpaper for Windows Lock Screen / Startup")
except Exception as e:
    print(f"[-] Could not set Lock Screen image: {e}")

# 6. Apply custom icons to standard User Folders via desktop.ini
user_folders = {
    'Documents': 'documents.ico',
    'Downloads': 'downloads.ico',
    'Pictures': 'pictures.ico',
    'Music': 'music.ico',
    'Videos': 'videos.ico'
}

for folder_name, ico_name in user_folders.items():
    paths_to_check = [
        os.path.join(user_profile, 'OneDrive', folder_name),
        os.path.join(user_profile, folder_name)
    ]
    for p in paths_to_check:
        if os.path.exists(p) and os.path.isdir(p):
            try:
                ini_path = os.path.join(p, 'desktop.ini')
                ico_path = os.path.join(icons_dest, ico_name)
                # Unhide
                if os.path.exists(ini_path):
                    ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x80)
                with open(ini_path, 'w', encoding='utf-8') as ini:
                    ini.write(f"[.ShellClassInfo]\nIconResource={ico_path},0\n[ViewState]\nMode=\nVid=\nFolderType=Generic\n")
                ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x02 | 0x04) # Hidden + System
                ctypes.windll.kernel32.SetFileAttributesW(p, 0x01) # ReadOnly required for folder
                print(f"[+] Folder customized: {p} -> {ico_name}")
            except Exception as e:
                print(f"[-] Could not customize {p}: {e}")

# 7. Shortcut Icon Mapping Table
wscript = win32com.client.Dispatch("WScript.Shell")

icon_mapping = {
    'chrome': 'google_chrome.ico',
    'google chrome': 'google_chrome.ico',
    'edge': 'microsoft_edge.ico',
    'microsoft edge': 'microsoft_edge.ico',
    'store': 'microsoft_store.ico',
    'microsoft store': 'microsoft_store.ico',
    'settings': 'settings.ico',
    'terminal': 'terminal.ico',
    'powershell': 'terminal.ico',
    'command prompt': 'terminal.ico',
    'file explorer': 'file_explorer.ico',
    'explorer': 'file_explorer.ico',
    'notepad': 'notepad.ico',
    'task manager': 'task_manager.ico',
    'telegram': 'telegram.ico',
    'whatsapp': 'whatsapp.ico',
    'spotify': 'spotify.ico',
    'steam': 'steam.ico',
    'visual studio code': 'visual_studio_code.ico',
    'code': 'visual_studio_code.ico',
    'cursor': 'visual_studio_code.ico',
    'antigravity': 'visual_studio_code.ico',
    'vlc': 'vlc.ico',
    'wireshark': 'wireshark.ico',
    'proton vpn': 'proton.ico',
    'proton mail': 'proton.ico',
    'proton drive': 'proton.ico',
    'bluestacks': 'bluestacks.ico',
    'pycharm': 'pycharm.ico',
    'rustrover': 'pycharm.ico',
    'brave': 'brave.ico',
    'adobe': 'adobe.ico',
    'acrobat': 'adobe.ico',
    'virtualbox': 'virtualbox.ico',
    'free download manager': 'fdm.ico',
    'fdm': 'fdm.ico',
    'calculator': 'calculator.ico',
    'photos': 'photos.ico',
    'paint': 'paint.ico',
    'clock': 'clock.ico',
    'outlook': 'outlook.ico',
    'cisco': 'cisco.ico',
    'dmss': 'cisco.ico',
    'eclipse': 'eclipse.ico',
    'tor': 'tor.ico',
    'minitool': 'minitool.ico',
    'z-library': 'documents.ico',
    'recycle': 'recycle_bin.ico',
    'github': 'github.ico',
    'copilot': 'github.ico',
    'mylio': 'photos.ico',
    'capcut': 'terminal.ico',
}

def match_icon(name):
    name_lower = name.lower()
    for key, ico in icon_mapping.items():
        if key in name_lower:
            return os.path.join(icons_dest, ico)
    return None

# 8. Apply to Desktop Shortcuts
desktop_dirs = [
    os.path.join(user_profile, 'OneDrive', 'Desktop'),
    os.path.join(user_profile, 'Desktop')
]

for d_dir in desktop_dirs:
    if os.path.exists(d_dir):
        for f in os.listdir(d_dir):
            if f.endswith('.lnk'):
                lnk_path = os.path.join(d_dir, f)
                base = os.path.splitext(f)[0]
                matched_ico = match_icon(base)
                if matched_ico and os.path.exists(matched_ico):
                    try:
                        shortcut = wscript.CreateShortcut(lnk_path)
                        shortcut.IconLocation = f"{matched_ico},0"
                        shortcut.Save()
                        print(f"[+] Updated Desktop shortcut: {f} -> {os.path.basename(matched_ico)}")
                    except Exception as e:
                        print(f"[-] Could not update {f}: {e}")

# 9. Apply to Start Menu Shortcuts
start_dirs = [
    os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs'),
]

for s_dir in start_dirs:
    if os.path.exists(s_dir):
        for root, dirs, files in os.walk(s_dir):
            for f in files:
                if f.endswith('.lnk'):
                    lnk_path = os.path.join(root, f)
                    base = os.path.splitext(f)[0]
                    matched_ico = match_icon(base)
                    if matched_ico and os.path.exists(matched_ico):
                        try:
                            shortcut = wscript.CreateShortcut(lnk_path)
                            shortcut.IconLocation = f"{matched_ico},0"
                            shortcut.Save()
                            print(f"[+] Updated Start Menu shortcut: {f} -> {os.path.basename(matched_ico)}")
                        except Exception as e:
                            pass

# 10. Copy system start menu shortcuts to user start menu and theme them
sys_start = os.path.expandvars(r'%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs')
user_start = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs')

if os.path.exists(sys_start):
    for root, dirs, files in os.walk(sys_start):
        for f in files:
            if f.endswith('.lnk') and not any(x in f.lower() for x in ['uninstall', 'help', 'readme', 'license']):
                base = os.path.splitext(f)[0]
                matched_ico = match_icon(base)
                if matched_ico and os.path.exists(matched_ico):
                    target_user_lnk = os.path.join(user_start, f)
                    try:
                        src_lnk = os.path.join(root, f)
                        orig = wscript.CreateShortcut(src_lnk)
                        new_sc = wscript.CreateShortcut(target_user_lnk)
                        new_sc.TargetPath = orig.TargetPath
                        new_sc.Arguments = orig.Arguments
                        new_sc.WorkingDirectory = orig.WorkingDirectory
                        new_sc.IconLocation = f"{matched_ico},0"
                        new_sc.Save()
                        print(f"[+] Created themed user Start shortcut for: {f}")
                    except Exception as e:
                        pass

# 11. Notify Windows Shell of association & icon changes
SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000
ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
print("[+] SHChangeNotify invoked: Windows Shell refreshed!")
print("=======================================================")
print("[+] Full System Customization Applied Successfully!")
print("=======================================================")
