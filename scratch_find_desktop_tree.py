import win32gui
import win32process
import ctypes

output = []

def enum_child(hwnd, extra):
    cls = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    extra.append((hwnd, cls, title))
    return True

def enum_top(hwnd, extra):
    cls = win32gui.GetClassName(hwnd)
    title = win32gui.GetWindowText(hwnd)
    if cls in ['Progman', 'WorkerW', 'SHELLDLL_DefView']:
        children = []
        win32gui.EnumChildWindows(hwnd, enum_child, children)
        extra.append((hwnd, cls, title, children))
    return True

top_wins = []
win32gui.EnumWindows(enum_top, top_wins)

with open(r"c:\Users\bhara\OneDrive\Documents\llll\desktop_structure.txt", "w", encoding="utf-8") as f:
    for hwnd, cls, title, children in top_wins:
        f.write(f"Top: {hwnd} ({hex(hwnd)}) | {cls} | '{title}'\n")
        for ch, ch_cls, ch_title in children:
            f.write(f"   Child: {ch} ({hex(ch)}) | {ch_cls} | '{ch_title}'\n")
