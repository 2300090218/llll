import os
import time
import win32com.client

ss_status = r"c:\Users\bhara\OneDrive\Documents\llll\ss_status.txt"
if os.path.exists(ss_status):
    os.remove(ss_status)

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
target = r"c:\Users\bhara\OneDrive\Documents\llll\take_screenshot.py"
py_exe = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\python.exe"
in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process \'{py_exe}\' -ArgumentList \'{target}\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("Launched elevated screenshot:", out.ReturnValue, "PID:", out.ProcessId)

for _ in range(15):
    time.sleep(0.5)
    if os.path.exists(ss_status):
        with open(ss_status) as f:
            print("Status:", f.read())
        break
else:
    print("Timeout waiting for screenshot status.")
