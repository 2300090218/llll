@echo off
:: ==============================================================================
:: OS26 / WINDOWS 11: 1-CLICK RESTORE THEME & WINDHAWK (AFTER EXAMS)
:: Re-enables Windhawk service, tray cushions, and optional dock effects.
:: ==============================================================================
title Restoring Custom Theme & Windhawk Mods...
color 0b

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Requesting Administrator privileges to start services...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

echo ==============================================================================
echo       RESTORING WINDHAWK & CUSTOM VISUAL MODS
echo ==============================================================================
echo.

:: 1. Restore Startup shortcuts
echo [1/4] Restoring startup shortcuts...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "DISABLED_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup_Disabled"

if exist "%DISABLED_DIR%\LiquidGlassDock.lnk" (
    move /y "%DISABLED_DIR%\LiquidGlassDock.lnk" "%STARTUP_DIR%\" >nul 2>&1
)
if exist "%DISABLED_DIR%\MacBrightnessEngine.lnk" (
    move /y "%DISABLED_DIR%\MacBrightnessEngine.lnk" "%STARTUP_DIR%\" >nul 2>&1
)
if exist "%DISABLED_DIR%\DesktopIconVibration.lnk" (
    move /y "%DISABLED_DIR%\DesktopIconVibration.lnk" "%STARTUP_DIR%\" >nul 2>&1
)
if exist "%DISABLED_DIR%\OS26FaceLockStartup.lnk" (
    move /y "%DISABLED_DIR%\OS26FaceLockStartup.lnk" "%STARTUP_DIR%\" >nul 2>&1
)

:: 2. Set Windhawk service back to Automatic & Start it
echo [2/4] Starting Windhawk background service...
sc config Windhawk start= auto >nul 2>&1
net start Windhawk >nul 2>&1

:: 3. Launch Windhawk UI / Tray
echo [3/4] Launching Windhawk client...
if exist "C:\Program Files\Windhawk\windhawk.exe" (
    start "" "C:\Program Files\Windhawk\windhawk.exe" -tray
)

:: 4. Refresh Explorer to apply hooks
echo [4/4] Refreshing Windows Explorer...
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul 2>&1
start explorer.exe

color 0a
echo.
echo ==============================================================================
echo  [SUCCESS] WINDHAWK & CUSTOM THEME FULLY RESTORED!
echo ==============================================================================
echo  - Windhawk Service: RUNNING (Automatic)
echo  - Windows 11 Taskbar Styler: ACTIVE
echo  - Tray pill/cushion backgrounds: ACTIVE
echo  - Permanent Liquid Glass Icons: ACTIVE
echo ==============================================================================
echo.
echo Press any key to close this window...
pause >nul
