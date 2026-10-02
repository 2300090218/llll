import win32com.client
import os
import subprocess

exe_path = r"C:\Program Files\WindowsApps\28017CharlesMilette.TranslucentTB_2026.1.0.0_x64__v826wp6bftszj\TranslucentTB.exe"

try:
    wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
    proc = wmi.Get("Win32_Process")
    in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
    in_params.CommandLine = r'explorer.exe "shell:AppsFolder\28017CharlesMilette.TranslucentTB_v826wp6bftszj!App"'
    out = proc.ExecMethod_("Create", in_params)
    print("WMI Exec:", out.ReturnValue, "PID:", out.ProcessId)
except Exception as e:
    print("WMI Error:", e)
