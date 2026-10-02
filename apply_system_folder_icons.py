import os
import shutil
import winreg
import ctypes
from ctypes import wintypes

icons_src = r'c:\Users\bhara\OneDrive\Documents\llll\Icons\ico'
icons_dest = r'C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons'
os.makedirs(icons_dest, exist_ok=True)

# 1. Copy all folder icons
for f in os.listdir(icons_src):
    if f.endswith('.ico'):
        shutil.copy2(os.path.join(icons_src, f), os.path.join(icons_dest, f))

# 2. Register Shell Icons (Default & Open Folders for all of Windows File Explorer)
folder_closed_ico = os.path.join(icons_dest, 'folder_closed.ico')
folder_open_ico = os.path.join(icons_dest, 'folder_open.ico')

shell_icons_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons')
winreg.SetValueEx(shell_icons_key, '3', 0, winreg.REG_SZ, f'{folder_closed_ico},0')
winreg.SetValueEx(shell_icons_key, '4', 0, winreg.REG_SZ, f'{folder_open_ico},0')
winreg.CloseKey(shell_icons_key)
print("[+] Registered global Shell Icons 3 & 4 (Folder Closed & Open)")

# 3. Apply custom icons to standard User Folders via desktop.ini
user_profile = os.environ['USERPROFILE']
user_folders = {
    'Documents': 'documents.ico',
    'Downloads': 'downloads.ico',
    'Pictures': 'pictures.ico',
    'Music': 'music.ico',
    'Videos': 'videos.ico',
    'Desktop': 'start_menu.ico'
}

for folder_name, ico_name in user_folders.items():
    # Check OneDrive path or user profile path
    paths_to_try = [
        os.path.join(user_profile, 'OneDrive', folder_name),
        os.path.join(user_profile, folder_name)
    ]
    for p in paths_to_try:
        if os.path.exists(p) and os.path.isdir(p):
            try:
                ini_path = os.path.join(p, 'desktop.ini')
                ico_path = os.path.join(icons_dest, ico_name)
                # Unhide if exists
                ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x80) # FILE_ATTRIBUTE_NORMAL
                with open(ini_path, 'w', encoding='utf-8') as ini:
                    ini.write(f"[.ShellClassInfo]\nIconResource={ico_path},0\n[ViewState]\nMode=\nVid=\nFolderType=Generic\n")
                # Set desktop.ini to System + Hidden
                ctypes.windll.kernel32.SetFileAttributesW(ini_path, 0x02 | 0x04) # HIDDEN | SYSTEM
                # Mark folder as Read-Only (Required by Windows to process desktop.ini!)
                ctypes.windll.kernel32.SetFileAttributesW(p, 0x01) # READONLY
                print(f"[+] Customized user folder: {p} -> {ico_name}")
            except Exception as e:
                print(f"[-] Could not update {p}: {e}")

# 4. Notify Shell of association change
SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000
ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)
print("[+] SHChangeNotify invoked: File Explorer refreshed!")
