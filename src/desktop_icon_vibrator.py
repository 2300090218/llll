"""
Desktop Icon Vibration Engine for Windows 11
Smooth, organic tactile shake/vibration for selected desktop icons.
Masks LVS_AUTOARRANGE and LVS_EX_SNAPTOGRID for sub-pixel accuracy.
Zero CPU usage when idle. Full drag-and-drop & multi-select compatibility.
"""

import os
import sys
import time
import math
import struct
import json
import signal
import atexit
import ctypes
from ctypes import wintypes
import psutil

# Win32 API setup
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

LVM_GETITEMCOUNT = 0x1004
LVM_SETITEMPOSITION = 0x100F
LVM_GETITEMPOSITION = 0x1010
LVM_GETNEXTITEM = 0x100C
LVM_GETSELECTEDCOUNT = 0x1032
LVM_SETEXTENDEDLISTVIEWSTYLE = 0x1036
LVM_GETEXTENDEDLISTVIEWSTYLE = 0x1037
LVNI_SELECTED = 0x0002

LVS_AUTOARRANGE = 0x0100
LVS_EX_SNAPTOGRID = 0x00080000
GWL_STYLE = -16
VK_LBUTTON = 0x01

PROCESS_VM_OPERATION = 0x0008
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
MEM_COMMIT = 0x1000
MEM_RELEASE = 0x8000
PAGE_READWRITE = 0x04

GetWindowLongPtr = user32.GetWindowLongPtrW if hasattr(user32, 'GetWindowLongPtrW') else user32.GetWindowLongW
SetWindowLongPtr = user32.SetWindowLongPtrW if hasattr(user32, 'SetWindowLongPtrW') else user32.SetWindowLongW

GetWindowLongPtr.argtypes = [ctypes.c_void_p, ctypes.c_int]
GetWindowLongPtr.restype = ctypes.c_ssize_t
SetWindowLongPtr.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_ssize_t]
SetWindowLongPtr.restype = ctypes.c_ssize_t

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "desktop_icon_vibration_config.json")
PID_FILE = os.path.join(SCRIPT_DIR, "desktop_icon_vibrator.pid")
LOG_FILE = os.path.join(SCRIPT_DIR, "vibrator_log.txt")

DEFAULT_CONFIG = {
    "enabled": True,
    "amplitude_x": 3.5,
    "amplitude_y": 2.8,
    "frequency_hz": 32.0,
    "secondary_frequency_hz": 60.0,
    "organic_stagger": 1.61803398875,
    "fps": 60,
    "pause_on_mouse_down": True
}

def log(msg):
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except Exception:
        pass

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                merged = dict(DEFAULT_CONFIG)
                merged.update(cfg)
                return merged
        except Exception:
            pass
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
    except Exception:
        pass
    return dict(DEFAULT_CONFIG)

def attach_desktop():
    """Attaches process and thread to WinSta0\\Default to interact with desktop windows."""
    try:
        hwinsta = user32.OpenWindowStationW('WinSta0', False, 0x10000000)
        if hwinsta:
            user32.SetProcessWindowStation(hwinsta)
        hdesk = user32.OpenDesktopW('Default', 0, False, 0x10000000)
        if hdesk:
            user32.SetThreadDesktop(hdesk)
    except Exception:
        pass

def find_desktop_listview():
    """Locates the SysListView32 handle for Windows Desktop."""
    attach_desktop()
    progman = user32.FindWindowW('Progman', None)
    defview = user32.FindWindowExW(progman, 0, 'SHELLDLL_DefView', None)
    if not defview:
        def enum_win(hwnd, lparam):
            dv = user32.FindWindowExW(hwnd, 0, 'SHELLDLL_DefView', None)
            if dv:
                result.append(dv)
                return False
            return True
        result = []
        WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
        user32.EnumWindows(WNDENUMPROC(enum_win), 0)
        if result:
            defview = result[0]
    if defview:
        return user32.FindWindowExW(defview, 0, 'SysListView32', None)
    return None

def make_lparam(x, y):
    return ((int(y) & 0xFFFF) << 16) | (int(x) & 0xFFFF)

class DesktopIconVibrator:
    def __init__(self):
        self.lv = None
        self.hproc = None
        self.remote_buf = None
        self.orig_style = None
        self.orig_ex_style = None
        self.styles_masked = False
        self.anchors = {} # idx -> (x, y)
        self.config = load_config()
        self.last_config_check = time.time()
        self.start_time = time.time()
        self.running = True
        self.mouse_was_down = False
        self.setup_signal_handlers()

    def setup_signal_handlers(self):
        try:
            signal.signal(signal.SIGINT, self.cleanup_and_exit)
            signal.signal(signal.SIGTERM, self.cleanup_and_exit)
        except Exception:
            pass
        atexit.register(self.cleanup)

    def init_handles(self):
        self.cleanup()
        self.lv = find_desktop_listview()
        if not self.lv:
            return False

        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(self.lv, ctypes.byref(pid))
        if not pid.value:
            return False

        self.hproc = kernel32.OpenProcess(
            PROCESS_VM_OPERATION | PROCESS_VM_READ | PROCESS_VM_WRITE,
            False,
            pid.value
        )
        if not self.hproc:
            return False

        self.remote_buf = kernel32.VirtualAllocEx(
            self.hproc, None, 32, MEM_COMMIT, PAGE_READWRITE
        )
        if not self.remote_buf:
            kernel32.CloseHandle(self.hproc)
            self.hproc = None
            return False

        self.orig_style = GetWindowLongPtr(self.lv, GWL_STYLE)
        self.orig_ex_style = user32.SendMessageW(self.lv, LVM_GETEXTENDEDLISTVIEWSTYLE, 0, 0)
        self.styles_masked = False
        log(f"Initialized desktop ListView 0x{self.lv:X}, Explorer PID {pid.value}")
        return True

    def get_item_position(self, idx):
        if not self.lv or not self.hproc or not self.remote_buf:
            return None
        res = user32.SendMessageW(self.lv, LVM_GETITEMPOSITION, idx, self.remote_buf)
        if not res:
            return None
        local_buf = ctypes.create_string_buffer(16)
        read_bytes = ctypes.c_size_t()
        ok = kernel32.ReadProcessMemory(self.hproc, self.remote_buf, local_buf, 8, ctypes.byref(read_bytes))
        if not ok or read_bytes.value < 8:
            return None
        return struct.unpack("ii", local_buf.raw[:8])

    def set_item_position(self, idx, x, y):
        if not self.lv:
            return
        user32.SendMessageW(self.lv, LVM_SETITEMPOSITION, idx, make_lparam(x, y))

    def mask_styles(self):
        """Temporarily mask LVS_AUTOARRANGE and LVS_EX_SNAPTOGRID to allow free oscillation."""
        if not self.styles_masked and self.lv:
            current_style = GetWindowLongPtr(self.lv, GWL_STYLE)
            if current_style & LVS_AUTOARRANGE:
                SetWindowLongPtr(self.lv, GWL_STYLE, current_style & ~LVS_AUTOARRANGE)
            # Mask out LVS_EX_SNAPTOGRID
            user32.SendMessageW(self.lv, LVM_SETEXTENDEDLISTVIEWSTYLE, LVS_EX_SNAPTOGRID, 0)
            self.styles_masked = True

    def unmask_styles(self):
        """Restore original auto-arrange and snap-to-grid styles."""
        if self.styles_masked and self.lv:
            if self.orig_style is not None:
                SetWindowLongPtr(self.lv, GWL_STYLE, self.orig_style)
            if self.orig_ex_style is not None and (self.orig_ex_style & LVS_EX_SNAPTOGRID):
                user32.SendMessageW(self.lv, LVM_SETEXTENDEDLISTVIEWSTYLE, LVS_EX_SNAPTOGRID, LVS_EX_SNAPTOGRID)
            self.styles_masked = False

    def restore_all_anchors(self):
        for idx, (ax, ay) in list(self.anchors.items()):
            self.set_item_position(idx, ax, ay)
        self.anchors.clear()

    def get_selected_indices(self):
        if not self.lv:
            return []
        items = []
        idx = -1
        while True:
            idx = user32.SendMessageW(self.lv, LVM_GETNEXTITEM, idx, LVNI_SELECTED)
            if idx == -1:
                break
            items.append(idx)
        return items

    def cleanup(self):
        try:
            self.restore_all_anchors()
            self.unmask_styles()
            if self.hproc and self.remote_buf:
                kernel32.VirtualFreeEx(self.hproc, self.remote_buf, 0, MEM_RELEASE)
                self.remote_buf = None
            if self.hproc:
                kernel32.CloseHandle(self.hproc)
                self.hproc = None
        except Exception:
            pass

    def cleanup_and_exit(self, signum=None, frame=None):
        self.running = False
        self.cleanup()
        if os.path.exists(PID_FILE):
            try:
                os.remove(PID_FILE)
            except Exception:
                pass
        sys.exit(0)

    def run(self):
        with open(PID_FILE, "w") as f:
            f.write(str(os.getpid()))

        log(f"Desktop Icon Vibrator running (PID {os.getpid()}).")

        while self.running:
            if not self.lv or not user32.IsWindow(self.lv):
                if not self.init_handles():
                    time.sleep(1.0)
                    continue

            now = time.time()
            # Periodically reload configuration if user modified JSON
            if now - self.last_config_check > 2.0:
                self.last_config_check = now
                self.config = load_config()

            if not self.config.get("enabled", True):
                if self.anchors:
                    self.restore_all_anchors()
                    self.unmask_styles()
                time.sleep(0.5)
                continue

            sel_count = user32.SendMessageW(self.lv, LVM_GETSELECTEDCOUNT, 0, 0)
            if sel_count == 0:
                if self.anchors:
                    self.restore_all_anchors()
                    self.unmask_styles()
                # Idle state: minimal CPU usage
                time.sleep(0.04)
                continue

            # Check mouse button state
            mouse_down = (user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000) != 0

            # If user just released the mouse, update anchors in case an icon was dragged to a new spot
            if self.mouse_was_down and not mouse_down:
                for idx in list(self.anchors.keys()):
                    pos = self.get_item_position(idx)
                    if pos:
                        self.anchors[idx] = pos
            self.mouse_was_down = mouse_down

            # While mouse is held down (dragging an icon or selecting area), hold at anchors
            if mouse_down and self.config.get("pause_on_mouse_down", True):
                for idx, (ax, ay) in self.anchors.items():
                    self.set_item_position(idx, ax, ay)
                time.sleep(0.03)
                continue

            # Mask auto-arrange & snap-to-grid so icons can vibrate freely
            self.mask_styles()

            # Query currently selected items
            current_selected = set(self.get_selected_indices())

            # Handle deselected items: restore to resting anchor and untrack
            for idx in list(self.anchors.keys()):
                if idx not in current_selected:
                    ax, ay = self.anchors[idx]
                    self.set_item_position(idx, ax, ay)
                    del self.anchors[idx]

            # Handle newly selected items: capture initial resting anchor
            for idx in current_selected:
                if idx not in self.anchors:
                    pos = self.get_item_position(idx)
                    if pos:
                        self.anchors[idx] = pos

            if not self.anchors:
                time.sleep(0.02)
                continue

            # Vibration parameters
            amp_x = float(self.config.get("amplitude_x", 3.5))
            amp_y = float(self.config.get("amplitude_y", 2.8))
            freq = float(self.config.get("frequency_hz", 32.0))
            sec_freq = float(self.config.get("secondary_frequency_hz", 60.0))
            stagger = float(self.config.get("organic_stagger", 1.61803398875))
            fps = max(15, min(120, int(self.config.get("fps", 60))))
            dt = 1.0 / fps

            elapsed = now - self.start_time

            # Compute organic displacement for each selected icon
            for idx in current_selected:
                if idx not in self.anchors:
                    continue
                ax, ay = self.anchors[idx]
                phase = idx * stagger

                # Dual sine wave combination for rich tactile flutter
                wave_x = math.sin(elapsed * (freq * 2 * math.pi) + phase) * amp_x + \
                         math.sin(elapsed * (sec_freq * 2 * math.pi) + phase * 0.7) * (amp_x * 0.25)
                wave_y = math.cos(elapsed * (freq * 1.15 * 2 * math.pi) + phase * 1.3) * amp_y + \
                         math.cos(elapsed * (sec_freq * 1.2 * 2 * math.pi)) * (amp_y * 0.25)

                dx = int(round(wave_x))
                dy = int(round(wave_y))

                self.set_item_position(idx, ax + dx, ay + dy)

            time.sleep(dt)

if __name__ == "__main__":
    try:
        log("Launching vibrator daemon...")
        vibrator = DesktopIconVibrator()
        vibrator.run()
    except Exception as e:
        import traceback
        log(f"Fatal error: {e}\n{traceback.format_exc()}")
        sys.exit(1)
