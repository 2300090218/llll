import os
import win32com.client

wsh = win32com.client.Dispatch("WScript.Shell")

desktop = os.path.expanduser(r"~\OneDrive\Desktop")
if not os.path.exists(desktop):
    desktop = os.path.expanduser(r"~\Desktop")

workspace = r"c:\Users\bhara\OneDrive\Documents\llll"

# 1. Desktop shortcut for START
start_bat = os.path.join(workspace, "START_DESKTOP_ICON_VIBRATION.bat")
sc_start = wsh.CreateShortcut(os.path.join(desktop, "Enable Icon Vibration.lnk"))
sc_start.TargetPath = start_bat
sc_start.WorkingDirectory = workspace
sc_start.IconLocation = r"C:\Windows\System32\shell32.dll,238"
sc_start.Description = "Start Desktop Icon Vibration Engine"
sc_start.Save()
print("Created Desktop shortcut for Start:", sc_start.FullName)

# 2. Desktop shortcut for STOP
stop_bat = os.path.join(workspace, "STOP_DESKTOP_ICON_VIBRATION.bat")
sc_stop = wsh.CreateShortcut(os.path.join(desktop, "Disable Icon Vibration.lnk"))
sc_stop.TargetPath = stop_bat
sc_stop.WorkingDirectory = workspace
sc_stop.IconLocation = r"C:\Windows\System32\shell32.dll,131"
sc_stop.Description = "Stop Desktop Icon Vibration Engine"
sc_stop.Save()
print("Created Desktop shortcut for Stop:", sc_stop.FullName)

# 3. Startup Shortcut so it runs automatically on logon
startup = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
sc_startup = wsh.CreateShortcut(os.path.join(startup, "DesktopIconVibration.lnk"))
sc_startup.TargetPath = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
sc_startup.Arguments = f'"{os.path.join(workspace, "desktop_icon_vibrator.py")}"'
sc_startup.WorkingDirectory = workspace
sc_startup.IconLocation = r"C:\Windows\System32\shell32.dll,238"
sc_startup.Description = "Windows Desktop Icon Vibration Engine"
sc_startup.Save()
print("Created Windows Startup shortcut:", sc_startup.FullName)
