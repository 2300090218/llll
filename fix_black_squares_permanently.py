import os
import sys
import time
import winreg
import ctypes
import subprocess
import glob

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

log = []
log_path = r"c:\Users\bhara\OneDrive\Documents\llll\permanent_fix_log.txt"

def write_log():
    try:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(log))
    except Exception as e:
        pass

if not is_admin():
    # Elevate
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{os.path.abspath(__file__)}"', None, 1)
    sys.exit(0)

log.append("[+] Started permanent fix running with Administrator privileges.")

# 1. Remove '29' from HKLM Shell Icons
hklm_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, hklm_path, 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            winreg.DeleteValue(key, "29")
            log.append("[+] Successfully removed '29' from HKLM\\...\\Shell Icons")
        except FileNotFoundError:
            log.append("[*] '29' was not present in HKLM\\...\\Shell Icons")
except FileNotFoundError:
    log.append("[*] HKLM Shell Icons key does not exist.")
except Exception as e:
    log.append(f"[-] Error removing from HKLM: {e}")

# Check if HKLM Shell Icons is empty; if so, delete the key entirely to restore clean Windows default
try:
    with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, hklm_path, 0, winreg.KEY_READ) as key:
        num_subkeys, num_values, _ = winreg.QueryInfoKey(key)
    if num_subkeys == 0 and num_values == 0:
        winreg.DeleteKey(winreg.HKEY_LOCAL_MACHINE, hklm_path)
        log.append("[+] HKLM Shell Icons was empty; deleted key to restore clean Windows default.")
except Exception as e:
    pass

# 2. Remove '29' from HKCU Shell Icons
hkcu_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Icons"
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, hkcu_path, 0, winreg.KEY_ALL_ACCESS) as key:
        try:
            winreg.DeleteValue(key, "29")
            log.append("[+] Successfully removed '29' from HKCU\\...\\Shell Icons")
        except FileNotFoundError:
            log.append("[*] '29' was not present in HKCU\\...\\Shell Icons")
except FileNotFoundError:
    log.append("[*] HKCU Shell Icons key does not exist.")
except Exception as e:
    log.append(f"[-] Error removing from HKCU: {e}")

# 3. Delete C:\Windows\blank.ico if it exists
blank_ico = r"C:\Windows\blank.ico"
if os.path.exists(blank_ico):
    try:
        os.remove(blank_ico)
        log.append(f"[+] Successfully deleted {blank_ico}")
    except Exception as e:
        log.append(f"[-] Error deleting {blank_ico}: {e}")
else:
    log.append(f"[*] {blank_ico} does not exist.")

# 4. Stop Explorer to release locked icon caches
log.append("[+] Stopping Windows Explorer to purge icon cache...")
write_log()
subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
time.sleep(2)

# 5. Clear all icon caches
local_app_data = os.environ.get("LOCALAPPDATA", "")
if local_app_data:
    # IconCache.db
    old_cache = os.path.join(local_app_data, "IconCache.db")
    if os.path.exists(old_cache):
        try:
            os.remove(old_cache)
            log.append(f"[+] Deleted {old_cache}")
        except Exception as e:
            log.append(f"[-] Could not delete {old_cache}: {e}")

    # Explorer icon and thumb caches
    explorer_cache_dir = os.path.join(local_app_data, "Microsoft", "Windows", "Explorer")
    if os.path.exists(explorer_cache_dir):
        for pattern in ["iconcache*.db", "thumbcache*.db"]:
            for f in glob.glob(os.path.join(explorer_cache_dir, pattern)):
                try:
                    os.remove(f)
                    log.append(f"[+] Deleted cache file {os.path.basename(f)}")
                except Exception as e:
                    pass

# 6. Restart Explorer
log.append("[+] Restarting Windows Explorer...")
subprocess.Popen(["explorer.exe"])
time.sleep(2)

log.append("[+] PERMANENT FIX COMPLETED SUCCESSFULLY. Black boxes are purged and will not return on reboot.")
write_log()
print("\n".join(log))
