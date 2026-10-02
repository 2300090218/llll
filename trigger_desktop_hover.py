import os
import time
import win32com.client

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\desktop_hover_log.txt"
if os.path.exists(log_path):
    try:
        os.remove(log_path)
    except:
        pass

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
bat_path = r"c:\Users\bhara\OneDrive\Documents\llll\apply_desktop_hover_style.bat"

in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process cmd.exe -ArgumentList \'/c {bat_path}\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("Trigger return:", out.ReturnValue, "PID:", out.ProcessId)

for i in range(15):
    time.sleep(1)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "DESKTOP ICON HOVER HIGHLIGHT & GLOW SUCCESSFULLY APPLIED" in content:
                print("Log output:\n" + content)
                break
else:
    print("Triggered batch elevation.")
