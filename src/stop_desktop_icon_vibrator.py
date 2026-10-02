import os
import time
import psutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PID_FILE = os.path.join(SCRIPT_DIR, "desktop_icon_vibrator.pid")

def stop():
    stopped = False

    # 1. Kill via PID file if present
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read().strip())
            if psutil.pid_exists(pid):
                p = psutil.Process(pid)
                p.terminate()
                try:
                    p.wait(timeout=2)
                except psutil.TimeoutExpired:
                    p.kill()
                stopped = True
                print(f"Terminated desktop icon vibrator (PID {pid}).")
        except Exception as e:
            print(f"PID termination notice: {e}")
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass

    # 2. Kill any remaining processes running desktop_icon_vibrator.py
    current_pid = os.getpid()
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['pid'] == current_pid:
                continue
            cmdline = " ".join(proc.info['cmdline'] or [])
            if "desktop_icon_vibrator.py" in cmdline:
                print(f"Stopping vibrator process PID {proc.info['pid']}...")
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except psutil.TimeoutExpired:
                    proc.kill()
                stopped = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    if stopped:
        print("Desktop icon vibrator stopped. Desktop icons restored to resting positions.")
    else:
        print("Desktop icon vibrator is not running.")

if __name__ == "__main__":
    stop()
