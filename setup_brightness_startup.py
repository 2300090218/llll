import os
import win32com.client

vbs_lines = [
    'Set WshShell = CreateObject("WScript.Shell")',
    'WshShell.CurrentDirectory = "c:\\Users\\bhara\\OneDrive\\Documents\\llll"',
    'WshShell.Run "C:\\Users\\bhara\\AppData\\Local\\Programs\\Python\\Python312\\pythonw.exe ""c:\\Users\\bhara\\OneDrive\\Documents\\llll\\mac_brightness_engine.py""", 0, False\n'
]
vbs_path = r"c:\Users\bhara\OneDrive\Documents\llll\launch_mac_brightness.vbs"
with open(vbs_path, "w", encoding="utf-8") as f:
    f.write("\n".join(vbs_lines))

wsh = win32com.client.Dispatch("WScript.Shell")
startup_dir = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
sc_path = os.path.join(startup_dir, "MacBrightnessEngine.lnk")
sc = wsh.CreateShortcut(sc_path)
sc.TargetPath = r"C:\Windows\System32\wscript.exe"
sc.Arguments = f'"{vbs_path}"'
sc.WorkingDirectory = r"c:\Users\bhara\OneDrive\Documents\llll"
sc.Description = "MacBook and Linux Style 0% Brightness Blackout Engine"
sc.Save()
print("Created startup shortcut:", sc_path)
