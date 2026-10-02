import os
import shutil
import ctypes
from ctypes import wintypes

workspace = r"c:\Users\bhara\OneDrive\Documents\llll"
desktop = os.path.expanduser(r"~\OneDrive\Desktop")
if not os.path.exists(desktop):
    desktop = os.path.expanduser(r"~\Desktop")

target_folder = os.path.join(desktop, "OS26 Tools")
os.makedirs(target_folder, exist_ok=True)

# List of items built in this project that are on the desktop
project_desktop_items = [
    "1_ENTER_EXAM_MODE.bat",
    "2_RESTORE_WINDHAWK_THEME.bat",
    "INSTALL_AND_APPLY_OS26_WINDHAWK.bat",
    "Enable Icon Vibration.lnk",
    "Disable Icon Vibration.lnk",
    "Liquid Glass Dock.lnk",
]

moved_items = []
for item in project_desktop_items:
    src = os.path.join(desktop, item)
    dst = os.path.join(target_folder, item)
    if os.path.exists(src):
        # Move to target folder
        shutil.move(src, dst)
        moved_items.append(item)
        print(f"Moved to OS26 Tools: {item}")

# Also copy convenient workspace batch files into OS26 Tools for easy access
workspace_tools = [
    "START_DESKTOP_ICON_VIBRATION.bat",
    "STOP_DESKTOP_ICON_VIBRATION.bat",
]
for tool in workspace_tools:
    src = os.path.join(workspace, tool)
    dst = os.path.join(target_folder, tool)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src, dst)
        print(f"Copied tool: {tool}")

# Apply custom OS26 Liquid Glass Folder Icon via desktop.ini
icon_path = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons\folder_closed.ico"
desktop_ini = os.path.join(target_folder, "desktop.ini")

# If desktop.ini already exists, clear attributes before overwriting
if os.path.exists(desktop_ini):
    try:
        os.system(f'attrib -h -s "{desktop_ini}"')
    except Exception:
        pass

ini_content = f"""[.ShellClassInfo]
IconResource={icon_path},0
[ViewState]
Mode=
Vid=
FolderType=Generic
"""

with open(desktop_ini, "w", encoding="ansi") as f:
    f.write(ini_content)

# In Windows, folder must have Read-Only attribute for desktop.ini to be read by Explorer
os.system(f'attrib +r "{target_folder}"')
# desktop.ini must be Hidden and System
os.system(f'attrib +h +s "{desktop_ini}"')

# Notify shell of changes
SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000
ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)

print(f"\nSuccessfully organized {len(moved_items)} project items into: {target_folder}")
