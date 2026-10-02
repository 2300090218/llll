@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title Installing Desktop Icon Hover Highlight Style
echo [*] Installing Desktop Icon Selection & Hover Glow Style in Windhawk...
python c:\Users\bhara\OneDrive\Documents\llll\install_desktop_icon_hover_style.py
echo.
pause
