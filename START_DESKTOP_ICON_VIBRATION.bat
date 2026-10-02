@echo off
title Desktop Icon Vibration Launcher
cd /d "c:\Users\bhara\OneDrive\Documents\llll"

python start_desktop_icon_vibrator.py

echo.
echo =====================================================================
echo  DESKTOP ICON VIBRATION IS ACTIVE!
echo  - Click any desktop icon, or select multiple icons, or press Ctrl+A
echo  - The selected icons will smoothly vibrate / shake!
echo  - Click on empty space to deselect: icons instantly return to rest!
echo  - To stop, double click STOP_DESKTOP_ICON_VIBRATION.bat
echo =====================================================================
ping 127.0.0.1 -n 4 >nul
