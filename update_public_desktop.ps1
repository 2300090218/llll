$wsh = New-Object -ComObject WScript.Shell
$icons = 'C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons_Shining'
$map = @{
    'Adobe Acrobat.lnk'             = "$icons\adobe_acrobat.ico"
    'BlueStacks 5.lnk'              = "$icons\bluestacks_5.ico"
    'BlueStacks Manager.lnk'        = "$icons\bluestacks_manager.ico"
    'Microsoft Edge.lnk'             = "$icons\microsoft_edge.ico"
    'MiniTool Partition Wizard.lnk' = "$icons\minitool_partition_wizard.ico"
    'MiniTool ShadowMaker.lnk'      = "$icons\minitool_shadowmaker.ico"
    'Oracle VirtualBox.lnk'         = "$icons\oracle_virtualbox.ico"
    'Proton VPN.lnk'                = "$icons\proton_vpn.ico"
    'PyCharm 2026.1.2.lnk'          = "$icons\pycharm_202612.ico"
    'VLC media player.lnk'          = "$icons\vlc_media_player.ico"
    'Windhawk.lnk'                  = "$icons\windhawk.ico"
    'Wireshark.lnk'                 = "$icons\wireshark.ico"
    'Z-Library.lnk'                 = "$icons\z-library.ico"
}

$log = @()
foreach ($k in $map.Keys) {
    $lnk = "C:\Users\Public\Desktop\$k"
    if (Test-Path $lnk) {
        try {
            $sc = $wsh.CreateShortcut($lnk)
            $sc.IconLocation = "$($map[$k]),0"
            $sc.Save()
            $log += "[+] Updated Public Desktop shortcut: $k -> $($map[$k])"
        } catch {
            $log += "[-] Error on $k : $_"
        }
    }
}

# Also update Windhawk Start Menu, File Explorer, and Settings stylers with shining border
$shiningBorder = '<LinearGradientBrush StartPoint="0.04,-0.14" EndPoint="1.22,1.10"><GradientStop Offset="0.10" Color="#90FFFFFF"/><GradientStop Offset="0.50" Color="#50A0E0FF"/><GradientStop Offset="0.95" Color="#15FFFFFF"/></LinearGradientBrush>'

# 1. Start Menu Styler
$smPath = 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-start-menu-styler\Settings'
Set-ItemProperty -Path $smPath -Name 'styleConstants[8]' -Value "BorderBrush=$shiningBorder" -ErrorAction SilentlyContinue
Set-ItemProperty -Path $smPath -Name 'styleConstants[9]' -Value "ElementBorderBrush=$shiningBorder" -ErrorAction SilentlyContinue
$now = [int][double]::Parse((Get-Date -UFormat %s))
Set-ItemProperty -Path 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-start-menu-styler' -Name 'SettingsChangeTime' -Value $now -ErrorAction SilentlyContinue
$log += "[+] Updated Start Menu Styler with shining edge"

# 2. File Explorer Styler
$fePath = 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler\Settings'
Set-ItemProperty -Path $fePath -Name 'styleConstants[2]' -Value "BorderBrush=$shiningBorder" -ErrorAction SilentlyContinue
Set-ItemProperty -Path $fePath -Name 'styleConstants[3]' -Value "ElementBorderBrush=$shiningBorder" -ErrorAction SilentlyContinue
Set-ItemProperty -Path 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-file-explorer-styler' -Name 'SettingsChangeTime' -Value $now -ErrorAction SilentlyContinue
$log += "[+] Updated File Explorer Styler with shining edge"

# 3. Settings Styler
$setPath = 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-settings-styler\Settings'
Set-ItemProperty -Path $setPath -Name 'styleConstants[2]' -Value "BorderBrush=$shiningBorder" -ErrorAction SilentlyContinue
Set-ItemProperty -Path 'HKLM:\Software\Windhawk\Engine\Mods\windows-11-settings-styler' -Name 'SettingsChangeTime' -Value $now -ErrorAction SilentlyContinue
$log += "[+] Updated Settings Styler with shining edge"

$log | Out-File -FilePath 'c:\Users\bhara\OneDrive\Documents\llll\public_desktop_update_log.txt' -Encoding utf8
Write-Output ($log -join "`n")
