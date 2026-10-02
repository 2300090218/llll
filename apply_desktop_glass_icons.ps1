$iconsDir = "C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons"
if (-not (Test-Path $iconsDir)) {
    New-Item -ItemType Directory -Path $iconsDir -Force | Out-Null
}

Copy-Item "c:\Users\bhara\OneDrive\Documents\llll\Icons\ico\*.ico" $iconsDir -Force

$wsh = New-Object -ComObject WScript.Shell
$desktop = "C:\Users\bhara\OneDrive\Desktop"

# Map apps to icons
$mappings = @{
    "Brave" = "google_chrome.ico"
    "Neo Browser" = "google_chrome.ico"
    "Tor Browser" = "search.ico"
    "GitHub Copilot" = "github.ico"
    "Antigravity IDE" = "visual_studio_code.ico"
    "Eclipse IDE" = "terminal.ico"
    "Proton Mail" = "discord.ico"
    "gnmail'gmail" = "google_chrome.ico"
    "Adobe Express Photos" = "snipping_tool.ico"
    "CapCut" = "spotify.ico"
    "DMSS" = "task_manager.ico"
    "Cisco Packet Tracer" = "settings.ico"
}

Get-ChildItem -Path $desktop -Filter "*.lnk" | ForEach-Object {
    $lnkPath = $_.FullName
    $name = $_.BaseName
    foreach ($key in $mappings.Keys) {
        if ($name -like "*$key*") {
            $icoFile = Join-Path $iconsDir $mappings[$key]
            if (Test-Path $icoFile) {
                try {
                    $shortcut = $wsh.CreateShortcut($lnkPath)
                    $shortcut.IconLocation = "$icoFile,0"
                    $shortcut.Save()
                    Write-Host "[+] Updated shortcut: $name -> $($mappings[$key])"
                } catch {
                    Write-Warning "Could not update shortcut: $name"
                }
            }
            break
        }
    }
}

# Create Core OS26 Liquid Glass Dock shortcuts on Desktop
$dockShortcuts = @(
    @{ Name = "Google Chrome"; Target = "chrome.exe"; Fallback = "msedge.exe"; Ico = "google_chrome.ico" },
    @{ Name = "File Explorer"; Target = "explorer.exe"; Ico = "file_explorer.ico" },
    @{ Name = "Settings"; Target = "explorer.exe"; Args = "ms-settings:"; Ico = "settings.ico" },
    @{ Name = "Terminal"; Target = "wt.exe"; Fallback = "cmd.exe"; Ico = "terminal.ico" },
    @{ Name = "Notepad"; Target = "notepad.exe"; Ico = "notepad.ico" },
    @{ Name = "Task Manager"; Target = "taskmgr.exe"; Ico = "task_manager.ico" },
    @{ Name = "Microsoft Store"; Target = "explorer.exe"; Args = "ms-windows-store:"; Ico = "microsoft_store.ico" }
)

foreach ($item in $dockShortcuts) {
    $targetPath = $item.Target
    $lnkFile = Join-Path $desktop "$($item.Name).lnk"
    $icoFile = Join-Path $iconsDir $item.Ico
    try {
        $sc = $wsh.CreateShortcut($lnkFile)
        $sc.TargetPath = $targetPath
        if ($item.Args) { $sc.Arguments = $item.Args }
        $sc.IconLocation = "$icoFile,0"
        $sc.Save()
        Write-Host "[+] Created OS26 Glass shortcut: $($item.Name)"
    } catch {
        Write-Warning "Failed to create $($item.Name)"
    }
}

# Refresh Shell Icon Cache
Write-Host "[+] Refreshing Windows icon cache..."
taskkill /f /im explorer.exe
Start-Sleep -Seconds 1
Remove-Item "$env:LOCALAPPDATA\IconCache.db" -Force -ErrorAction SilentlyContinue
Remove-Item "$env:LOCALAPPDATA\Microsoft\Windows\Explorer\iconcache*" -Force -ErrorAction SilentlyContinue
Start-Process explorer.exe
Start-Sleep -Seconds 2
Write-Host "[+] Explorer restarted with fresh icon cache!"
