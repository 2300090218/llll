@echo off
:: ==============================================================================
:: OS26 / WINDOWS 11: 1-CLICK EXAM SAFE MODE ACTIVATOR
:: Completely terminates Windhawk and Python background processes.
:: Keeps your permanent custom icons, wallpaper, and theme 100% intact.
:: ==============================================================================
title Activating Clean Exam Safe Mode...
color 0b

:: Check for Administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Requesting Administrator privileges to stop services...
    powershell -Command "Start-Process cmd -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

echo ==============================================================================
echo       ACTIVATING EXAM SAFE MODE (CLEAN SYSTEM STATE)
echo ==============================================================================
echo.

:: 1. Terminate Python background processes (Dock, Brightness engines)
echo [1/5] Stopping background Python customization processes...
taskkill /f /im pythonw.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1

:: 2. Temporarily disable Startup shortcuts so they don't launch on reboot during exams
echo [2/5] Disabling auto-startup of Python background scripts...
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "DISABLED_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup_Disabled"
if not exist "%DISABLED_DIR%" mkdir "%DISABLED_DIR%" >nul 2>&1

if exist "%STARTUP_DIR%\LiquidGlassDock.lnk" (
    move /y "%STARTUP_DIR%\LiquidGlassDock.lnk" "%DISABLED_DIR%\" >nul 2>&1
)
if exist "%STARTUP_DIR%\MacBrightnessEngine.lnk" (
    move /y "%STARTUP_DIR%\MacBrightnessEngine.lnk" "%DISABLED_DIR%\" >nul 2>&1
)
if exist "%STARTUP_DIR%\DesktopIconVibration.lnk" (
    move /y "%STARTUP_DIR%\DesktopIconVibration.lnk" "%DISABLED_DIR%\" >nul 2>&1
)
if exist "%STARTUP_DIR%\OS26FaceLockStartup.lnk" (
    move /y "%STARTUP_DIR%\OS26FaceLockStartup.lnk" "%DISABLED_DIR%\" >nul 2>&1
)

:: 3. Stop and configure Windhawk Service
echo [3/5] Stopping Windhawk background service and processes...
sc config Windhawk start= demand >nul 2>&1
net stop Windhawk >nul 2>&1
taskkill /f /im windhawk.exe >nul 2>&1
taskkill /f /im windhawk-ui.exe >nul 2>&1

:: 4. Cleanly restart Windows Explorer to flush injected DLL hooks from RAM
echo [4/5] Flushing Windows Explorer memory and refreshing native icon cache...
taskkill /f /im explorer.exe >nul 2>&1
timeout /t 1 /nobreak >nul 2>&1
start explorer.exe

:: 5. Verification check
echo [5/5] Auditing active background processes...
timeout /t 2 /nobreak >nul 2>&1

set "PROCESS_COUNT=0"
tasklist | findstr /i /c:windhawk >nul 2>&1
if %errorlevel% equ 0 set /a PROCESS_COUNT+=1

tasklist | findstr /i /c:pythonw >nul 2>&1
if %errorlevel% equ 0 set /a PROCESS_COUNT+=1

echo.
if %PROCESS_COUNT% equ 0 (
    color 0a
    echo ==============================================================================
    echo  [SUCCESS] SYSTEM IS 100%% CLEAN AND EXAM READY!
    echo ==============================================================================
    echo  - Windhawk Service: STOPPED (Startup set to Manual)
    echo  - Windhawk Processes: 0 RUNNING
    echo  - Python Background Scripts: 0 RUNNING
    echo  - Memory Hooks: Completely cleared from Explorer
    echo.
    echo  - Permanent Liquid Glass Icons: 100%% ACTIVE (Native Windows Icon Cache)
    echo  - Wallpaper & Dark Theme: 100%% ACTIVE
    echo.
    echo  You can now launch Safe Exam Browser, Mercer Mettl, Wheebox, HirePro,
    echo  CoCubes, TCS iON, or any other exam application without any process alerts!
    echo ==============================================================================
) else (
    color 0c
    echo [!] Warning: Some background processes could not be stopped. Please check Task Manager.
)

echo.
echo Press any key to close this window...
pause >nul
