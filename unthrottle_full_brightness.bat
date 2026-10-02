@echo off
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -NoProfile -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

title Intel DPST Disable and Full Peak Brightness Unlock
echo [*] Disabling Intel DPST auto-dimming in Registry...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v FeatureTestControl /t REG_DWORD /d 0x9250 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v Dpst6_3ApplyExtraDimming /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v PowerDpstAggressivenessLevel /t REG_DWORD /d 0 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000" /v DpstEpsmWeight /t REG_DWORD /d 0 /f

echo [*] Disabling Windows Adaptive Brightness in Powercfg...
powercfg -setacvalueindex SCHEME_CURRENT SUB_VIDEO ADAPTBRIGHT 0
powercfg -setdcvalueindex SCHEME_CURRENT SUB_VIDEO ADAPTBRIGHT 0
powercfg -setactive SCHEME_CURRENT

echo.
echo [+] SUCCESS! 100% Brightness is now unthrottled and will shine at true peak physical brightness with ZERO auto-dimming!
echo.
pause
