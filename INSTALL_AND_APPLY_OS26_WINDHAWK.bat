@echo off
setlocal EnableDelayedExpansion
title OS26 Liquid Glass Theme Installer for Windhawk

:: Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Requesting Administrator privileges to install Windhawk...
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

cls
echo =====================================================================
echo           OS26 LIQUID GLASS THEME FOR WINDOWS 11
echo           Based on WasiXGamer's Windows 11 Taskbar Styler
echo =====================================================================
echo.

set "THEME_DIR=c:\Users\bhara\OneDrive\Documents\llll"

echo [*] Step 1/3: Installing Windhawk silently...
if exist "%THEME_DIR%\windhawk_setup.exe" (
    "%THEME_DIR%\windhawk_setup.exe" /S
) else (
    echo [!] windhawk_setup.exe not found in %THEME_DIR%
)

timeout /t 5 /nobreak >nul

echo [*] Step 2/3: Checking Windhawk installation...
if exist "C:\Program Files\Windhawk\windhawk.exe" (
    echo [+] Windhawk successfully installed in C:\Program Files\Windhawk!
) else (
    echo [!] Windhawk installation in progress...
)

echo [*] Step 3/3: Opening Windhawk and theme configurations...
start "" "C:\Program Files\Windhawk\windhawk.exe"
explorer.exe "%THEME_DIR%\Windhawk_Configs"

echo.
echo =====================================================================
echo [+] HOW TO APPLY THE THEME IN WINDHAWK:
echo ---------------------------------------------------------------------
echo 1. In the Windhawk window that just opened, search for:
echo    "Windows 11 Taskbar Styler"
echo 2. Click "Details", then click "Install".
echo 3. In the mod's "Settings" tab:
echo    - Either choose "OS26 Liquid Glass" from the Themes dropdown!
echo    - OR click "Textual mode", copy the text from:
echo      Windhawk_Configs\Clear_MacDock.yaml, and click "Save settings"!
echo.
echo Optional MacDock companion mods:
echo - "Taskbar Dock Animation" (for smooth Mac-style bounce and hover zoom)
echo - "Taskbar Thumbnail Size" (size: 180)
echo =====================================================================
echo.
pause
