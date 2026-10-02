import win32gui
import win32process
import ctypes

def get_desktop_listview():
    progman = win32gui.FindWindow('Progman', None)
    defview = win32gui.FindWindowEx(progman, 0, 'SHELLDLL_DefView', None)
    if not defview:
        def enum_windows(hwnd, extra):
            p = win32gui.FindWindowEx(hwnd, 0, 'SHELLDLL_DefView', None)
            if p:
                extra.append(p)
            return True
        extra = []
        win32gui.EnumWindows(enum_windows, extra)
        if extra:
            defview = extra[0]
    if defview:
        lv = win32gui.FindWindowEx(defview, 0, 'SysListView32', None)
        return progman, defview, lv
    return progman, None, None

p, d, lv = get_desktop_listview()
with open(r"c:\Users\bhara\OneDrive\Documents\llll\desktop_lv_test.txt", "w") as f:
    f.write(f"Progman: {p}, DefView: {d}, ListView: {lv}\n")
    if lv:
        tid, pid = win32process.GetWindowThreadProcessId(lv)
        count = ctypes.windll.user32.SendMessageW(lv, 0x1004, 0, 0) # LVM_GETITEMCOUNT
        f.write(f"PID: {pid}, Item Count: {count}\n")
