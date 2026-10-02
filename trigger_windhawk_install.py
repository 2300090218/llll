import win32com.client

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
bat_path = r"C:\Users\bhara\OneDrive\Desktop\INSTALL_AND_APPLY_OS26_WINDHAWK.bat"
in_params.CommandLine = f'powershell.exe -WindowStyle Hidden -Command "Start-Process cmd.exe -ArgumentList \'/c \"\"\"{bat_path}\"\"\"\' -Verb RunAs"'
out = proc.ExecMethod_("Create", in_params)
print("WMI Trigger Return:", out.ReturnValue, "PID:", out.ProcessId)
