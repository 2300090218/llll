import win32com.client

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
target = r"c:\Users\bhara\OneDrive\Documents\llll\apply_notification_center_fix.py"
py_exe = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\python.exe"

in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process \'{py_exe}\' -ArgumentList \'{target}\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("Win+A fix trigger Return:", out.ReturnValue, "PID:", out.ProcessId)
