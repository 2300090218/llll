import os
import time
import win32com.client

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\dock_zoom_log.txt"
if os.path.exists(log_path):
    try:
        os.remove(log_path)
    except:
        pass

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
target = r"c:\Users\bhara\OneDrive\Documents\llll\install_and_apply_dock_zoom_and_highlight.py"
py_exe = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\python.exe"

in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process \'{py_exe}\' -ArgumentList \'{target}\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("Trigger return:", out.ReturnValue, "PID:", out.ProcessId)

for i in range(25):
    time.sleep(1)
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            if "TASKBAR DOCK ZOOM & HIGHLIGHT SUCCESSFULLY APPLIED" in content:
                print("Log output:\n" + content)
                break
else:
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            print("Partial Log output:\n" + f.read())
    else:
        print("Waiting for completion...")
