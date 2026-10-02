# OS26 Liquid Glass Theme for Windows 11

[![Platform](https://img.shields.io/badge/Platform-Windows%2011%20(22H2%20--%2026H2)-0078D4?logo=windows)](https://microsoft.com)
[![Architecture](https://img.shields.io/badge/Architecture-x64-30D158)]()
[![Design](https://img.shields.io/badge/Style-OS26%20Liquid%20Glass-00A4EF)]()
[![Version](https://img.shields.io/badge/Version-v2.6.0%20Pro-blueviolet)]()

An authentic, high-performance transformation suite that brings the **OS26 Liquid Glass** interface to Windows 11. It features a translucent glass dock, acrylic blur File Explorer, multi-harmonic desktop icon vibration, 50+ multi-resolution handcrafted liquid glass icons, a 4K Ice Frost background, and a 1-click Exam Safe Mode.

---

## 📸 Visual Overview

| Component | Visual Feature | Preview |
| :--- | :--- | :--- |
| **Liquid Glass Dock** | Interactive hover magnification, curved reflection, genuine app tiles | `assets/previews/screenshot-dock.png` |
| **Desktop Icon Vibration** | Dynamic tactile shake when selecting icons, zero idle CPU | Integrated daemon |
| **File Explorer Glass** | Acrylic blur, translucent tabs, glowing border highlights | `assets/previews/screenshot_fe.png` |
| **System Cleanliness** | Single `OS26 Tools` desktop folder, pristine 5-column grid | `assets/previews/screenshot_clean_desktop.png` |
| **Windhawk Mod Styler** | Clear MacDock, Clear Taskbar, Dark variants, thumbnail zoom | `Windhawk_Configs/` |

---

## 🚀 Quick Start & Installation

### Option 1: Using the Standalone Windows Installer (Recommended for Users)
1. Download `OS26-Liquid-Glass-Setup.exe` from the `dist/windows/` directory.
2. Run `OS26-Liquid-Glass-Setup.exe`.
3. Follow the modern installation wizard:
   - Choose whether to create a Desktop shortcut.
   - Choose whether to enable automatic background startup with Windows.
4. Click **Install**.
5. Once completed, check **Launch OS26 Liquid Glass Control Center** and click **Finish**.

> **Note on Dependencies:** The recipient does **NOT** need Python, Node.js, or any development SDKs installed. All runtimes, libraries, and assets are 100% self-contained in the installer.

---

## 💎 Core Features

### 1. Liquid Glass Control Center & Dashboard
- **Central Management Hub**: Monitor active engines, toggle features in real time, customize vibration intensity, and switch between Clear and Dark themes.
- **System Tray Integration**: Minimizes seamlessly to the system tray (`QSystemTrayIcon`) with a custom OS26 Liquid Glass icon and quick-access context menu.

### 2. Interactive Liquid Glass Dock
- High-FPS macOS-style magnification dock anchored to the bottom of the screen.
- Auto-extracts authentic Windows app shortcuts and composites them over OS26 translucent liquid glass tiles.
- Hover physics with smooth lerp scaling.

### 3. Tactile Desktop Icon Vibration Engine
- Oscillates selected desktop icons at high frequency (32 Hz + 60 Hz multi-harmonic wave) with golden-ratio phase stagger ($1.618$).
- **Sub-Pixel Grid Freedom**: Automatically masks `LVS_AUTOARRANGE` and `LVS_EX_SNAPTOGRID` so icons move smoothly.
- **Drag-and-Drop Safety**: Automatically pauses when left-clicking or dragging an icon, updating to the new drop position upon mouse release.
- **Zero Idle CPU**: Drops to **0.0% CPU usage** when no desktop icons are selected.

### 4. Windows 11 File Explorer Acrylic Styler
- Authentic `acrylicblur` translucent effect for File Explorer panels.
- Liquid glass tab headers, rounded active tab highlights, and luminous borders.

### 5. 1-Click Exam Safe Mode
- Instant 1-click toggle for students and test-takers:
  - Gracefully terminates Windhawk and Python background daemons.
  - Temporarily disables startup shortcuts.
  - Flushes Windows Explorer memory.
  - **100% Safe**: Safe Exam Browser (SEB), Mercer Mettl, Wheebox, HirePro, CoCubes, and TCS iON will not flag any active customization hooks.
  - Keeps permanent custom icons, 4K wallpaper, and desktop layout fully intact.

---

## 🛠️ Project Directory Structure

```
OS26-Liquid-Glass/
│
├── src/                               # Application source code
│   ├── os26_app.py                    # Main Control Center UI & System Tray daemon
│   ├── desktop_zoom_dock.py           # PyQt6 Liquid Glass Dock engine
│   ├── desktop_icon_vibrator.py       # Desktop icon vibration engine
│   ├── mac_brightness_engine.py       # 0-nit Mac-style brightness engine
│   ├── apply_full_system_customization.py # Shell icon and registry engine
│   ├── apply_fe_styles_elevated.py    # File Explorer acrylic styler
│   ├── install_and_style_all_mods.py  # Windhawk automated mod installer
│   ├── rebuild_icon_cache.py          # Native Windows shell refresh
│   └── exam_mode.py                   # Exam Safe Mode logic
│
├── assets/                            # Media and theme assets
│   ├── icons/                         # 50+ handcrafted 256x256 multi-res glass icons
│   ├── wallpaper/                     # OS26_Ice_Frost_Wallpaper_4K.jpg
│   ├── windhawk/                      # windhawk_setup.exe & YAML styling presets
│   └── previews/                      # Screenshots and preview images
│
├── scripts/                           # Standalone batch utilities
│   ├── ENTER_EXAM_MODE.bat            # 1-Click Exam Mode activator
│   ├── RESTORE_WINDHAWK_THEME.bat     # 1-Click Theme restorer
│   ├── START_DESKTOP_ICON_VIBRATION.bat # Standalone vibration launcher
│   ├── STOP_DESKTOP_ICON_VIBRATION.bat  # Standalone vibration stopper
│   └── organize_desktop_project_tools.py # Desktop cleanup utility
│
├── installer/                         # Windows installer configuration
│   └── setup.iss                      # Inno Setup compiler definition
│
├── build.py                           # Automated reproducible master build pipeline
├── README.md                          # Documentation and user guide
│
└── dist/
    └── windows/
        └── OS26-Liquid-Glass-Setup.exe # Official shareable Windows Installer
```

---

## ⚙️ Building from Source

To compile the application and build the Windows installer yourself:

### Prerequisites
- Windows 11 (64-bit)
- Python 3.10+ with `pyinstaller`, `PyQt6`, `Pillow`, `psutil`, `pywin32`, `pyyaml`
- Inno Setup 6 (`ISCC.exe`)

### Reproducible Build Command
```cmd
python build.py
```
This script will:
1. Validate and assemble all icons, configs, and assets.
2. Compile `src/os26_app.py` into a standalone application directory using PyInstaller.
3. Package the complete binary distribution into `dist/windows/OS26-Liquid-Glass-Setup.exe` with Inno Setup.

---

## 🔒 Permissions & Security Architecture

- **Standard User Operations**: Daily operation of the Control Center, Desktop Dock, Icon Vibration, and Brightness engines runs entirely in user-space without requiring elevation.
- **Elevation via Standard Windows UAC**:
  - The installer requests Administrator privileges during setup to install cleanly into `{autopf}\OS26 Liquid Glass` and register Start Menu shortcuts.
  - When applying system-wide Windhawk hooks (writing to `HKLM:\Software\Windhawk\Engine\Mods`), Windows UAC prompts the user normally.
  - **No Security Bypasses**: The application does not bypass Windows security controls, disable UAC, or modify protected Windows system binaries.

---

## 🗑️ Uninstallation

To uninstall OS26 Liquid Glass:
1. Open Windows **Settings** > **Apps** > **Installed Apps**.
2. Locate **OS26 Liquid Glass Theme for Windows 11**.
3. Click the three dots and select **Uninstall**.
4. The uninstaller will cleanly remove all installed program files, shortcuts, and startup registrations.
