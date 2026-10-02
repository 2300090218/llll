import os
import sys
import winreg
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit(0)

log = []
log.append("[+] Running elevated battery optimization...")

# 1. Prevent Indexing On Battery
try:
    key_path = r"SOFTWARE\Policies\Microsoft\Windows\Windows Search"
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "PreventIndexingOnBattery", 0, winreg.REG_DWORD, 1)
    winreg.CloseKey(key)
    log.append("[+] Set PreventIndexingOnBattery = 1 (stops indexing CPU drain on battery)")
except Exception as e:
    log.append(f"[-] Error setting Windows Search policy: {e}")

# 2. Delivery Optimization on Battery (do not use peer bandwidth below 40% battery)
try:
    key_path = r"SOFTWARE\Policies\Microsoft\Windows\DeliveryOptimization"
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "DOMinBatteryPercentageAllowed", 0, winreg.REG_DWORD, 40)
    winreg.CloseKey(key)
    log.append("[+] Set DeliveryOptimization DOMinBatteryPercentageAllowed = 40")
except Exception as e:
    log.append(f"[-] Error setting DeliveryOptimization policy: {e}")

# 3. Ensure PowerThrottling is enabled (Execution State Optimization)
try:
    key_path = r"SYSTEM\CurrentControlSet\Control\Power\PowerThrottling"
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "PowerThrottlingOff", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)
    log.append("[+] Set PowerThrottlingOff = 0 (EcoQoS background CPU throttling enabled)")
except Exception as e:
    log.append(f"[-] Error setting PowerThrottling: {e}")

# 4. Run HP Battery Test if available
hp_diag = r"C:\Program Files\HP\HpHwDiag\HPDIAGS\BatteryCheckWrapperBase\BatteryTest.exe"
if os.path.exists(hp_diag):
    try:
        proc = subprocess.run([hp_diag], capture_output=True, text=True, timeout=10)
        log.append(f"[+] HP Battery Test executed (code {proc.returncode}):\nSTDOUT: {proc.stdout[:300]}\nSTDERR: {proc.stderr[:300]}")
    except Exception as e:
        log.append(f"[-] HP Battery Test run note: {e}")

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\battery_opt_log.txt"
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("\n".join(log))
