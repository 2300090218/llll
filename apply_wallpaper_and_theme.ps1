Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class WallpaperManager {
    [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
    public const int SPI_SETDESKWALLPAPER = 20;
    public const int SPIF_UPDATEINIFILE = 0x01;
    public const int SPIF_SENDCHANGE = 0x02;

    public static void SetWallpaper(string path) {
        SystemParametersInfo(SPI_SETDESKWALLPAPER, 0, path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE);
    }
}
"@

$themeDir = "C:\Users\bhara\AppData\Local\OS26_Liquid_Glass"
if (-not (Test-Path $themeDir)) {
    New-Item -ItemType Directory -Path $themeDir -Force | Out-Null
}

$wpSrc = "c:\Users\bhara\OneDrive\Documents\llll\OS26_Ice_Frost_Wallpaper_4K.jpg"
$wpDest = Join-Path $themeDir "OS26_Ice_Frost_Wallpaper_4K.jpg"
Copy-Item $wpSrc $wpDest -Force

# 1. Apply Wallpaper
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "Wallpaper" -Value $wpDest
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "WallpaperStyle" -Value "10" # Fill
Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "TileWallpaper" -Value "0"
[WallpaperManager]::SetWallpaper($wpDest)
Write-Host "[+] 4K Blue Ice Frost Wallpaper applied successfully!"

# 2. Apply Windows Dark Mode & Transparency
$personalizePath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
Set-ItemProperty -Path $personalizePath -Name "AppsUseLightTheme" -Value 0 -Type DWord
Set-ItemProperty -Path $personalizePath -Name "SystemUsesLightTheme" -Value 0 -Type DWord
Set-ItemProperty -Path $personalizePath -Name "EnableTransparency" -Value 1 -Type DWord
Write-Host "[+] Windows Dark Mode & Transparency enabled!"

# 3. Apply Accent Colors (Cyan Blue #00A4EF matching the theme start button)
$dwmPath = "HKCU:\Software\Microsoft\Windows\DWM"
Set-ItemProperty -Path $dwmPath -Name "AccentColor" -Value 0xFFA400 -Type DWord # ABGR for #00A4EF
Set-ItemProperty -Path $dwmPath -Name "ColorPrevalence" -Value 1 -Type DWord

# Update shell
rundll32.exe user32.dll,UpdatePerUserSystemParameters
Write-Host "[+] Theme colors and accents applied!"
