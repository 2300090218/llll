@echo off
title Stop Desktop Icon Vibration
cd /d "c:\Users\bhara\OneDrive\Documents\llll"

python stop_desktop_icon_vibrator.py

echo.
echo Desktop Icon Vibration has been terminated. All icons restored to resting grid.
ping 127.0.0.1 -n 4 >nul
