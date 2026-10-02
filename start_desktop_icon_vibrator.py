import os
import time
import win32com.client
from stop_desktop_icon_vibrator import stop

SCRIPT_DIR = r"c:\Users\bhara\OneDrive\Documents\llll"
PYW_EXE = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
TARGET_SCRIPT = os.path.join(SCRIPT_DIR, "desktop_icon_vibrator.py")
PID_FILE = os.path.join(SCRIPT_DIR, "desktop_icon_vibrator.pid")
LOG_FILE = os.path.join(SCRIPT_DIR, "vibrator_log.txt")

def start():
    # 1. Stop any running instance
    stop()
    time.sleep(0.5)

    # 2. Launch via WMI Win32_Process.Create to decouple from terminal/IDE session
    wmi = win32com.client.GetObject(r"winmgmts:\\.\root\cimv2")
    proc = wmi.Get("Win32_Process")
    in_params = proc.Methods_("Create").InParameters.SpawnInstance_()
    in_params.CurrentDirectory = SCRIPT_DIR
    in_params.CommandLine = f'"{PYW_EXE}" "{TARGET_SCRIPT}"'

    out = proc.ExecMethod_("Create", in_params)
    ret = out.ReturnValue
    pid = out.ProcessId
    print(f"Spawned vibrator daemon: ReturnValue={ret}, PID={pid}")

    # 3. Verify daemon is running
    for _ in range(30):
        time.sleep(0.1)
        if os.path.exists(PID_FILE):
            try:
                with open(PID_FILE, "r") as f:
                    running_pid = f.read().strip()
                print(f"Desktop Icon Vibrator is ACTIVE and running (PID: {running_pid})!")
                return True
            except Exception:
                pass

    print("Desktop Icon Vibrator process launched.")
    return ret == 0

if __name__ == "__main__":
    start()
