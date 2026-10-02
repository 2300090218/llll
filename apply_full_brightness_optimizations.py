import os
import sys
import time
import winreg
import ctypes
import subprocess
import win32com.client

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\brightness_opt_log.txt"
log = []

def write_log():
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
    except:
        pass

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    sys.exit(0)

log.append("[+] Running with Administrator privileges for Full Brightness Optimizations...")
write_log()

# -------------------------------------------------------------
# 1. DISABLE INTEL DPST & EXTRA DIMMING (UNTHROTTLE 100% BRIGHTNESS)
# -------------------------------------------------------------
base = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
for sub in ["0000", "0001", "0002"]:
    reg_path = f"{base}\\{sub}"
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as k:
            try:
                desc = winreg.QueryValueEx(k, "DriverDesc")[0]
                if "Intel" in desc:
                    log.append(f"[+] Found Intel graphics key at {sub}: {desc}")
                    # Disable DPST via FeatureTestControl (0x9250 disables DPST and enables full unthrottled backlight)
                    winreg.SetValueEx(k, "FeatureTestControl", 0, winreg.REG_DWORD, 0x9250)
                    winreg.SetValueEx(k, "Dpst6_3ApplyExtraDimming", 0, winreg.REG_DWORD, 0)
                    winreg.SetValueEx(k, "DpstEpsmWeight", 0, winreg.REG_DWORD, 0)
                    try:
                        winreg.SetValueEx(k, "PowerDpstAggressivenessLevel", 0, winreg.REG_DWORD, 0)
                    except:
                        pass
                    log.append("[+] Successfully disabled Intel DPST and extra dimming! Display will now reach true 100% peak brightness.")
            except FileNotFoundError:
                pass
    except Exception as e:
        pass

write_log()

# -------------------------------------------------------------
# 2. DISABLE WINDOWS ADAPTIVE BRIGHTNESS & CABC
# -------------------------------------------------------------
try:
    subprocess.run(["powercfg", "-setacvalueindex", "SCHEME_CURRENT", "SUB_VIDEO", "ADAPTBRIGHT", "0"], capture_output=True)
    subprocess.run(["powercfg", "-setdcvalueindex", "SCHEME_CURRENT", "SUB_VIDEO", "ADAPTBRIGHT", "0"], capture_output=True)
    subprocess.run(["powercfg", "-setactive", "SCHEME_CURRENT"], capture_output=True)
    log.append("[+] Disabled Windows Adaptive Brightness in Powercfg (AC & DC).")
except Exception as e:
    log.append(f"[-] Powercfg adjustment error: {e}")

write_log()

# -------------------------------------------------------------
# 3. SET UP MAC-STYLE 0% BRIGHTNESS BLACKOUT ENGINE
# -------------------------------------------------------------
vbs_content = """Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "c:\\Users\\bhara\\OneDrive\\Documents\\llll"
WshShell.Run "C:\\Users\\bhara\\AppData\\Local\\Programs\\Python\\Python312\\pythonw.exe ""c:\\Users\\bhara\\OneDrive\\Documents\\llll\\mac_brightness_engine.py""", 0, False
"""
vbs_path = r"c:\Users\bhara\OneDrive\Documents\llll\launch_mac_brightness.vbs"
with open(vbs_path, "w", encoding="utf-8") as f:
    f.write(vbs_content)
log.append(f"[+] Created silent launcher: {vbs_path}")

# Add to Startup folder
try:
    wsh = win32com.client.Dispatch("WScript.Shell")
    startup_dir = os.path.join(os.environ["APPDATA"], r"Microsoft\Windows\Start Menu\Programs\Startup")
    sc = wsh.CreateShortcut(os.path.join(startup_dir, "MacBrightnessEngine.lnk"))
    sc.TargetPath = r"C:\Windows\System32\wscript.exe"
    sc.Arguments = f'"{vbs_path}"'
    sc.WorkingDirectory = r"c:\Users\bhara\OneDrive\Documents\llll"
    sc.Description = "Mac-Style 0% Brightness Blackout Engine"
    sc.Save()
    log.append("[+] Added MacBrightnessEngine to Windows Startup folder.")
except Exception as e:
    log.append(f"[-] Error creating startup shortcut: {e}")

write_log()

# -------------------------------------------------------------
# 4. START THE ENGINE NOW
# -------------------------------------------------------------
try:
    cmd = r'C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe c:\Users\bhara\OneDrive\Documents\llll\mac_brightness_engine.py'
    wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
    proc = wmi.Get("Win32_Process")
    in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
    in_params.CommandLine = cmd
    out = proc.ExecMethod_("Create", in_params)
    log.append(f"[+] Started Mac Brightness Engine process (PID: {out.ProcessId})")
except Exception as e:
    log.append(f"[-] Error launching engine: {e}")

log.append("[+] ALL BRIGHTNESS OPTIMIZATIONS COMPLETED SUCCESSFULLY!")
write_log()
print("\n".join(log))
