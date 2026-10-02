import os
import win32com.client

wsh = win32com.client.Dispatch("WScript.Shell")

# 1. Desktop shortcut
desktop = os.path.expanduser(r"~\OneDrive\Desktop")
if not os.path.exists(desktop):
    desktop = os.path.expanduser(r"~\Desktop")

vbs_path = r"c:\Users\bhara\OneDrive\Documents\llll\launch_dock.vbs"
sc_path = os.path.join(desktop, "Liquid Glass Dock.lnk")
sc = wsh.CreateShortcut(sc_path)
sc.TargetPath = r"C:\Windows\System32\wscript.exe"
sc.Arguments = f'"{vbs_path}"'
sc.WorkingDirectory = r"c:\Users\bhara\OneDrive\Documents\llll"
sc.IconLocation = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons\start_menu.ico,0"
sc.Description = "OS26 Liquid Glass Desktop Zoom Dock"
sc.Save()
print("Created Desktop shortcut:", sc_path)

# 2. Startup shortcut
startup = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
start_sc_path = os.path.join(startup, "LiquidGlassDock.lnk")
sc2 = wsh.CreateShortcut(start_sc_path)
sc2.TargetPath = r"C:\Windows\System32\wscript.exe"
sc2.Arguments = f'"{vbs_path}"'
sc2.WorkingDirectory = r"c:\Users\bhara\OneDrive\Documents\llll"
sc2.IconLocation = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons\start_menu.ico,0"
sc2.Description = "OS26 Liquid Glass Desktop Zoom Dock"
sc2.Save()
print("Created Startup shortcut:", start_sc_path)
