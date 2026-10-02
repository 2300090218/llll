import os
import sys
import shutil
import winreg
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{__file__}"', None, 1)
    sys.exit(0)

log = []
log.append("[+] Running elevated...")

# 1. Copy blank.ico to C:\Windows\blank.ico
src = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons\blank.ico"
dst = r"C:\Windows\blank.ico"
try:
    shutil.copyfile(src, dst)
    log.append(f"[+] Copied {src} to {dst}")
except Exception as e:
    log.append(f"[-] Error copying {src} to {dst}: {e}")

# 2. Set HKLM Shell Icons\29
hklm_key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
try:
    key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, hklm_key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "29", 0, winreg.REG_SZ, r"C:\Windows\blank.ico")
    winreg.CloseKey(key)
    log.append(r"[+] Successfully set HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons\29 = C:\Windows\blank.ico")
except Exception as e:
    log.append(f"[-] Error setting HKLM key: {e}")

# 3. Set HKCU Shell Icons\29
hkcu_key_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
try:
    key = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, hkcu_key_path, 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "29", 0, winreg.REG_SZ, r"C:\Windows\blank.ico")
    winreg.CloseKey(key)
    log.append(r"[+] Successfully set HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons\29 = C:\Windows\blank.ico")
except Exception as e:
    log.append(f"[-] Error setting HKCU key: {e}")

log_path = r"c:\Users\bhara\OneDrive\Documents\llll\shortcut_arrow_log.txt"
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log))

print("\n".join(log))
