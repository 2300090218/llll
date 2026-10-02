import win32com.client

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
bat = r"c:\Users\bhara\OneDrive\Documents\llll\unthrottle_full_brightness.bat"
in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process cmd.exe -ArgumentList \'/c {bat}\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("WMI trigger return:", out.ReturnValue, "PID:", out.ProcessId)
