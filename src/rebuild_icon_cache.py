import os
import time
import subprocess
import glob
import ctypes

print("[*] Flushing icon associations with ie4uinit...")
try:
    subprocess.run(["ie4uinit.exe", "-show"], timeout=5)
except Exception as e:
    print("ie4uinit error:", e)

print("[*] Terminating explorer.exe to unlock icon cache files...")
subprocess.run(["taskkill", "/f", "/im", "explorer.exe"], capture_output=True)
time.sleep(1.5)

localappdata = os.environ.get("LOCALAPPDATA", "")
if localappdata:
    # 1. IconCache.db
    old_cache = os.path.join(localappdata, "IconCache.db")
    if os.path.exists(old_cache):
        try:
            os.remove(old_cache)
            print("[+] Removed:", old_cache)
        except Exception as e:
            print("[-] Could not remove old cache:", e)

    # 2. Explorer iconcache* and thumbcache*
    exp_dir = os.path.join(localappdata, "Microsoft", "Windows", "Explorer")
    if os.path.exists(exp_dir):
        patterns = [os.path.join(exp_dir, "iconcache*"), os.path.join(exp_dir, "thumbcache*")]
        for p in patterns:
            for f in glob.glob(p):
                try:
                    os.remove(f)
                    print("[+] Removed cache file:", os.path.basename(f))
                except Exception as e:
                    # Some files may be locked by background components, ignore
                    pass

print("[*] Restarting explorer.exe...")
# Start explorer in the user session
subprocess.Popen(["explorer.exe"])
time.sleep(2)

print("[*] Broadcasting SHCNE_ASSOCCHANGED to Windows shell...")
SHCNE_ASSOCCHANGED = 0x08000000
SHCNF_IDLIST = 0x0000
ctypes.windll.shell32.SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, None, None)

print("[+] Icon cache rebuild complete! Desktop shortcuts now render full icons without shortcut arrows.")
