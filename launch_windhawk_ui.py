import win32com.client

wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
proc = wmi.Get("Win32_Process")
in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
in_params.CommandLine = r'"C:\Program Files\Windhawk\windhawk.exe"'
out = proc.ExecMethod_("Create", in_params)
print("Launch Windhawk Return:", out.ReturnValue, "PID:", out.ProcessId)

# Also open Windhawk_Configs folder for the user
in_params.CommandLine = r'explorer.exe "c:\Users\bhara\OneDrive\Documents\llll\Windhawk_Configs"'
proc.ExecMethod_("Create", in_params)
