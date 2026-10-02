import os
import time
from PIL import ImageGrab
import ctypes

try:
    # Optional: Toggle Show Desktop so the desktop icons are clearly visible
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) # Win down
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0) # D down
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0) # D up
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) # Win up
    time.sleep(1.0)

    img = ImageGrab.grab()
    save_path = r"c:\Users\bhara\OneDrive\Documents\llll\screenshot_clean_desktop.png"
    img.save(save_path)
    with open(r"c:\Users\bhara\OneDrive\Documents\llll\ss_status.txt", "w") as f:
        f.write("OK: " + str(img.size))
except Exception as e:
    with open(r"c:\Users\bhara\OneDrive\Documents\llll\ss_status.txt", "w") as f:
        f.write("ERR: " + str(e))
