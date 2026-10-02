; Inno Setup Script for OS26 Liquid Glass Theme for Windows 11
; Produces dist\windows\OS26-Liquid-Glass-Setup.exe

#define MyAppName "OS26 Liquid Glass Theme for Windows 11"
#define MyAppVersion "2.6.0"
#define MyAppPublisher "WasiXGamer / OS26 Project"
#define MyAppExeName "OS26-Liquid-Glass.exe"

[Setup]
AppId={{E82F41D1-7A39-44F2-87DA-B1E5B7448A26}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\OS26 Liquid Glass
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=..\dist\windows
OutputBaseFilename=OS26-Liquid-Glass-Setup
SetupIconFile=..\assets\icons\start_menu.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Start OS26 Liquid Glass automatically when Windows starts (Minimizes to System Tray)"; GroupDescription: "System Integration:"; Flags: unchecked

[Files]
; Standalone Compiled Application Executable & Runtime
Source: "..\dist\bin\OS26-Liquid-Glass\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; Asset Libraries (Icons, Wallpaper, Windhawk Setup, Configs)
Source: "..\assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs

; Convenience Scripts & Tools
Source: "..\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\OS26 Liquid Glass Control Center"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\icons\start_menu.ico"
Name: "{group}\Enter Exam Safe Mode"; Filename: "{app}\scripts\ENTER_EXAM_MODE.bat"; IconFilename: "{app}\assets\icons\settings.ico"
Name: "{group}\Restore Full Theme"; Filename: "{app}\scripts\RESTORE_WINDHAWK_THEME.bat"; IconFilename: "{app}\assets\icons\start_menu.ico"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\OS26 Liquid Glass Control Center"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\assets\icons\start_menu.ico"; Tasks: desktopicon
Name: "{userstartup}\OS26 Liquid Glass"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--minimized"; Tasks: startup

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
