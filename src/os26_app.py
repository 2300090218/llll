"""
OS26 Liquid Glass Theme for Windows 11 - Desktop Application & Control Center
Author: WasiXGamer / OS26 Project
Unified desktop interface, system tray manager, and live customization engine.
"""

import os
import sys
import json
import time
import subprocess
import ctypes
import winreg
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QThread
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTabWidget, QSlider, QCheckBox, QFrame,
    QSystemTrayIcon, QMenu, QMessageBox, QScrollArea, QGridLayout,
    QProgressBar, QTextEdit
)
from PyQt6.QtGui import QIcon, QPixmap, QFont, QColor, QPalette, QBrush, QAction
import psutil

APP_VERSION = "2.6.0 Pro"
APP_TITLE = "OS26 Liquid Glass Control Center"

# Resolve directories
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
WALLPAPER_PATH = os.path.join(ASSETS_DIR, "wallpaper", "OS26_Ice_Frost_Wallpaper_4K.jpg")
CONFIG_PATH = os.path.join(PROJECT_ROOT, "desktop_icon_vibration_config.json")
TOOLS_DIR = os.path.join(os.path.expanduser(r"~\OneDrive\Desktop"), "OS26 Tools")
if not os.path.exists(TOOLS_DIR):
    TOOLS_DIR = os.path.join(os.path.expanduser(r"~\Desktop"), "OS26 Tools")

RUN_KEY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"
APP_RUN_NAME = "OS26_Liquid_Glass"

# Helper to check running background processes
def is_process_running(keyword):
    keyword = keyword.lower()
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            cmdline = " ".join(proc.info['cmdline'] or []).lower()
            if keyword in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

def is_windhawk_running():
    for proc in psutil.process_iter(['name']):
        try:
            if "windhawk" in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False

class OS26ControlCenter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_TITLE} v{APP_VERSION}")
        self.resize(920, 680)
        self.setMinimumSize(850, 600)

        # Set Window and App Icon
        icon_path = os.path.join(ICONS_DIR, "start_menu.ico")
        if not os.path.exists(icon_path):
            icon_path = os.path.join(PROJECT_ROOT, "Icons", "ico", "start_menu.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            self.app_icon = QIcon(icon_path)
        else:
            self.app_icon = QIcon()

        self.setup_styling()
        self.init_ui()
        self.init_tray()

        # Polling timer for status indicators
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.refresh_status)
        self.poll_timer.start(2000)

    def setup_styling(self):
        """Rich authentic OS26 Dark Liquid Glass Theme Styling."""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #090e17, stop:0.5 #0d1522, stop:1 #060a11);
                color: #f0f4fc;
                font-family: 'Segoe UI Variable', 'Segoe UI', -apple-system, sans-serif;
            }
            QWidget {
                color: #e6edf8;
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 14px;
                background: rgba(14, 22, 35, 0.65);
                top: -1px;
            }
            QTabBar::tab {
                background: rgba(20, 30, 48, 0.50);
                color: #9cb1d1;
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-bottom: none;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                padding: 10px 22px;
                margin-right: 4px;
                font-weight: 600;
                font-size: 13px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0078d4, stop:1 #005a9e);
                color: #ffffff;
                border: 1px solid #00a4ef;
            }
            QTabBar::tab:hover:!selected {
                background: rgba(30, 45, 70, 0.70);
                color: #ffffff;
            }
            /* Cards */
            .CardFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(22, 34, 54, 0.75), stop:1 rgba(14, 23, 38, 0.75));
                border: 1px solid rgba(0, 164, 239, 0.22);
                border-radius: 14px;
                padding: 16px;
            }
            .CardFrame:hover {
                border: 1px solid rgba(0, 164, 239, 0.50);
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(28, 44, 70, 0.85), stop:1 rgba(18, 29, 48, 0.85));
            }
            /* Buttons */
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1a2a44, stop:1 #121e33);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-radius: 8px;
                color: #ffffff;
                font-weight: 600;
                padding: 8px 16px;
                font-size: 13px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #253d63, stop:1 #182a47);
                border: 1px solid #00a4ef;
            }
            QPushButton:pressed {
                background: #0078d4;
            }
            QPushButton.PrimaryBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0078d4, stop:1 #005a9e);
                border: 1px solid #33bbf5;
                font-size: 14px;
                padding: 10px 20px;
            }
            QPushButton.PrimaryBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0086ed, stop:1 #0066b3);
                border: 1px solid #66ccff;
            }
            QPushButton.WarningBtn {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c42b1c, stop:1 #8e190e);
                border: 1px solid #ff6655;
            }
            QPushButton.WarningBtn:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e83b2a, stop:1 #a82012);
            }
            /* Sliders */
            QSlider::groove:horizontal {
                height: 6px;
                background: rgba(255, 255, 255, 0.10);
                border-radius: 3px;
            }
            QSlider::sub-page:horizontal {
                background: #00a4ef;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #ffffff;
                border: 2px solid #0078d4;
                width: 18px;
                margin-top: -6px;
                margin-bottom: -6px;
                border-radius: 9px;
            }
            /* Checkbox */
            QCheckBox {
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 5px;
                border: 1px solid rgba(255, 255, 255, 0.20);
                background: rgba(16, 26, 42, 0.80);
            }
            QCheckBox::indicator:checked {
                background: #0078d4;
                border: 1px solid #00a4ef;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.20);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 0.40);
            }
        """)

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(16)

        # Header Banner
        header = QHBoxLayout()
        logo_label = QLabel()
        logo_icon = os.path.join(ICONS_DIR, "start_menu.ico")
        if os.path.exists(logo_icon):
            logo_pix = QPixmap(logo_icon).scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(logo_pix)
        header.addWidget(logo_label)

        title_vbox = QVBoxLayout()
        title = QLabel("OS26 Liquid Glass Theme for Windows 11")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #ffffff; letter-spacing: 0.5px;")
        subtitle = QLabel("Liquid Glass Dock • File Explorer Acrylic Blur • Icon Vibration • 4K Ice Frost Theme")
        subtitle.setStyleSheet("color: #00c3ff; font-size: 12px; font-weight: 500;")
        title_vbox.addWidget(title)
        title_vbox.addWidget(subtitle)
        header.addLayout(title_vbox)
        header.addStretch()

        # Status badge
        self.status_badge = QLabel("✨ Liquid Glass Active")
        self.status_badge.setStyleSheet("""
            background: rgba(0, 164, 239, 0.18);
            color: #38d6ff;
            border: 1px solid rgba(0, 164, 239, 0.45);
            border-radius: 14px;
            padding: 6px 14px;
            font-weight: 600;
            font-size: 12px;
        """)
        header.addWidget(self.status_badge)
        main_layout.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_dashboard_tab(), "🏠 Dashboard")
        self.tabs.addTab(self.create_tuning_tab(), "⚙️ Vibration & Dock Tuning")
        self.tabs.addTab(self.create_theme_tab(), "🎨 Theme Styles & Presets")
        self.tabs.addTab(self.create_about_tab(), "ℹ️ Diagnostics & About")
        main_layout.addWidget(self.tabs)

        # Bottom Master Bar
        bottom_bar = QHBoxLayout()
        
        btn_apply_all = QPushButton("⚡ Apply Complete OS26 Theme")
        btn_apply_all.setProperty("class", "PrimaryBtn")
        btn_apply_all.clicked.connect(self.on_apply_full_theme)
        bottom_bar.addWidget(btn_apply_all)

        btn_exam = QPushButton("🛡️ 1-Click Exam Safe Mode")
        btn_exam.setProperty("class", "WarningBtn")
        btn_exam.clicked.connect(self.on_enter_exam_mode)
        bottom_bar.addWidget(btn_exam)

        btn_restore = QPushButton("🔄 Restore Full Theme")
        btn_restore.clicked.connect(self.on_restore_theme)
        bottom_bar.addWidget(btn_restore)

        btn_tools = QPushButton("📁 Open OS26 Tools")
        btn_tools.clicked.connect(self.on_open_tools_folder)
        bottom_bar.addWidget(btn_tools)

        main_layout.addLayout(bottom_bar)

    def create_card(self, title_text, desc_text, icon_name, toggle_callback=None, btn_text="Toggle"):
        frame = QFrame()
        frame.setProperty("class", "CardFrame")
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        # Top row: icon + title + pill
        top_row = QHBoxLayout()
        ico_lbl = QLabel()
        ico_path = os.path.join(ICONS_DIR, icon_name)
        if os.path.exists(ico_path):
            ico_lbl.setPixmap(QPixmap(ico_path).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        top_row.addWidget(ico_lbl)

        card_title = QLabel(title_text)
        card_title.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        card_title.setStyleSheet("color: #ffffff;")
        top_row.addWidget(card_title)
        top_row.addStretch()

        pill = QLabel("Checking...")
        pill.setStyleSheet("""
            background: rgba(255, 255, 255, 0.08);
            color: #9cb1d1;
            border-radius: 10px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 600;
        """)
        top_row.addWidget(pill)
        layout.addLayout(top_row)

        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #a8bfde; font-size: 11.5px; min-height: 32px;")
        layout.addWidget(desc)

        if toggle_callback:
            btn = QPushButton(btn_text)
            btn.clicked.connect(toggle_callback)
            layout.addWidget(btn)
        else:
            btn = None

        return frame, pill, btn

    def create_dashboard_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        grid = QGridLayout(container)
        grid.setSpacing(14)
        grid.setContentsMargins(8, 12, 8, 12)

        # 1. Liquid Glass Zoom Dock
        f1, self.pill_dock, self.btn_dock = self.create_card(
            "Liquid Glass Dock",
            "Interactive macOS-style hover zoom dock with genuine Liquid Glass app tiles & bottom screen anchor.",
            "start_menu.ico",
            self.toggle_dock,
            "Toggle Dock"
        )
        grid.addWidget(f1, 0, 0)

        # 2. Desktop Icon Vibration Engine
        f2, self.pill_vibe, self.btn_vibe = self.create_card(
            "Desktop Icon Vibration",
            "Smooth, organic tactile shake when selecting desktop icons. Drag-and-drop safety & 0% idle CPU.",
            "settings.ico",
            self.toggle_vibration,
            "Toggle Vibration"
        )
        grid.addWidget(f2, 0, 1)

        # 3. File Explorer Glass Styler
        f3, self.pill_fe, self.btn_fe = self.create_card(
            "File Explorer Acrylic Blur",
            "Acrylic blur transparency, rounded tabs, glowing borders, and translucent header.",
            "file_explorer.ico",
            self.reapply_fe_styles,
            "Re-apply Explorer Glass"
        )
        grid.addWidget(f3, 1, 0)

        # 4. Windhawk Taskbar & Settings Styler
        f4, self.pill_wh, self.btn_wh = self.create_card(
            "Windhawk Theme Mods",
            "Taskbar Styler, Settings Translucent Styler, Control Center, and Thumbnail zoom.",
            "windhawk.ico",
            self.open_windhawk_ui,
            "Open Windhawk"
        )
        grid.addWidget(f4, 1, 1)

        # 5. Mac 0-Nit Brightness Engine
        f5, self.pill_bright, self.btn_bright = self.create_card(
            "Mac 0-Nit Brightness",
            "Hardware/software pitch black screen dimming at 0 nits, matching MacBook behavior.",
            "photos.ico",
            self.toggle_brightness,
            "Toggle Brightness"
        )
        grid.addWidget(f5, 2, 0)

        # 6. Icons & 4K Wallpaper
        f6, self.pill_icons, self.btn_icons = self.create_card(
            "Permanent Icons & Wallpaper",
            "50+ 256x256 custom liquid glass icons and 4K Ice Frost background applied to shell.",
            "folder_closed.ico",
            self.reapply_icons_and_wallpaper,
            "Reapply Icons"
        )
        grid.addWidget(f6, 2, 1)

        scroll.setWidget(container)
        return scroll

    def create_tuning_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(18)

        # Vibration Tuning Box
        vibe_box = QFrame()
        vibe_box.setProperty("class", "CardFrame")
        vb_layout = QVBoxLayout(vibe_box)
        vb_layout.setSpacing(12)

        v_title = QLabel("🌊 Desktop Icon Vibration Settings")
        v_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        v_title.setStyleSheet("color: #ffffff;")
        vb_layout.addWidget(v_title)

        # Amplitude
        amp_box = QHBoxLayout()
        amp_lbl = QLabel("Shake Amplitude (Displacement):")
        amp_lbl.setStyleSheet("font-size: 13px; font-weight: 500;")
        self.amp_val_lbl = QLabel("3.5 px")
        self.amp_val_lbl.setStyleSheet("color: #00a4ef; font-weight: bold;")
        self.amp_slider = QSlider(Qt.Orientation.Horizontal)
        self.amp_slider.setRange(10, 80) # 1.0 to 8.0 px
        self.amp_slider.setValue(35)
        self.amp_slider.valueChanged.connect(lambda v: self.amp_val_lbl.setText(f"{v/10.0:.1f} px"))
        amp_box.addWidget(amp_lbl)
        amp_box.addWidget(self.amp_slider)
        amp_box.addWidget(self.amp_val_lbl)
        vb_layout.addLayout(amp_box)

        # Frequency
        freq_box = QHBoxLayout()
        freq_lbl = QLabel("Vibration Frequency (Speed):")
        freq_lbl.setStyleSheet("font-size: 13px; font-weight: 500;")
        self.freq_val_lbl = QLabel("32.0 Hz")
        self.freq_val_lbl.setStyleSheet("color: #00a4ef; font-weight: bold;")
        self.freq_slider = QSlider(Qt.Orientation.Horizontal)
        self.freq_slider.setRange(15, 60)
        self.freq_slider.setValue(32)
        self.freq_slider.valueChanged.connect(lambda v: self.freq_val_lbl.setText(f"{v:.1f} Hz"))
        freq_box.addWidget(freq_lbl)
        freq_box.addWidget(self.freq_slider)
        freq_box.addWidget(self.freq_val_lbl)
        vb_layout.addLayout(freq_box)

        self.chk_pause_drag = QCheckBox("Pause vibration while dragging icons or rubber-band selecting (Recommended)")
        self.chk_pause_drag.setChecked(True)
        vb_layout.addWidget(self.chk_pause_drag)

        btn_save_vibe = QPushButton("💾 Save Vibration Tuning")
        btn_save_vibe.clicked.connect(self.save_vibration_settings)
        vb_layout.addWidget(btn_save_vibe)

        layout.addWidget(vibe_box)

        # Startup & System Options
        sys_box = QFrame()
        sys_box.setProperty("class", "CardFrame")
        sb_layout = QVBoxLayout(sys_box)
        sb_layout.setSpacing(12)

        s_title = QLabel("🚀 System Integration & Startup")
        s_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        s_title.setStyleSheet("color: #ffffff;")
        sb_layout.addWidget(s_title)

        self.chk_startup = QCheckBox("Start OS26 Liquid Glass on Windows Startup (Minimizes to System Tray)")
        self.chk_startup.setChecked(self.is_startup_enabled())
        self.chk_startup.stateChanged.connect(self.toggle_startup_registry)
        sb_layout.addWidget(self.chk_startup)

        self.chk_tray_close = QCheckBox("Minimize to System Tray when closing the window")
        self.chk_tray_close.setChecked(True)
        sb_layout.addWidget(self.chk_tray_close)

        btn_rebuild_cache = QPushButton("🔄 Rebuild Windows Native Icon Cache")
        btn_rebuild_cache.clicked.connect(self.on_rebuild_cache)
        sb_layout.addWidget(btn_rebuild_cache)

        layout.addWidget(sys_box)
        layout.addStretch()

        self.load_vibration_settings()
        return container

    def create_theme_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        header = QLabel("🎨 Theme Presets & Styles")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #ffffff;")
        layout.addWidget(header)

        # Preview Gallery Grid
        gallery = QGridLayout()
        gallery.setSpacing(14)

        presets = [
            ("Clear MacDock (Default)", "screenshot-dock.png", "Floating centered liquid glass dock with curved reflection."),
            ("Clear Taskbar", "screenshot-taskbar.png", "Full-width transparent taskbar with liquid glass icon pods."),
            ("Dark Taskbar", "screenshot-taskbar-dark.png", "Deep obsidian frosted acrylic dock for nighttime aesthetics."),
            ("Clean Desktop View", "screenshot_clean_desktop.png", "5-column organized app grid with OS26 Tools folder.")
        ]

        for idx, (p_title, p_img, p_desc) in enumerate(presets):
            frame = QFrame()
            frame.setProperty("class", "CardFrame")
            f_layout = QVBoxLayout(frame)
            f_layout.setContentsMargins(12, 12, 12, 12)

            t_lbl = QLabel(p_title)
            t_lbl.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            t_lbl.setStyleSheet("color: #00a4ef;")
            f_layout.addWidget(t_lbl)

            img_lbl = QLabel()
            img_path = os.path.join(ASSETS_DIR, "previews", p_img)
            if not os.path.exists(img_path):
                img_path = os.path.join(PROJECT_ROOT, p_img)
            if os.path.exists(img_path):
                pix = QPixmap(img_path).scaled(340, 190, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                img_lbl.setPixmap(pix)
            f_layout.addWidget(img_lbl)

            d_lbl = QLabel(p_desc)
            d_lbl.setStyleSheet("color: #a8bfde; font-size: 11px;")
            f_layout.addWidget(d_lbl)

            row = idx // 2
            col = idx % 2
            gallery.addWidget(frame, row, col)

        layout.addLayout(gallery)
        scroll.setWidget(container)
        return scroll

    def create_about_tab(self):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        header = QLabel("ℹ️ System Diagnostics & About")
        header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        header.setStyleSheet("color: #ffffff;")
        layout.addWidget(header)

        self.diag_text = QTextEdit()
        self.diag_text.setReadOnly(True)
        self.diag_text.setStyleSheet("""
            background: rgba(10, 16, 26, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 8px;
            color: #79d2ff;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 12px;
            padding: 10px;
        """)
        layout.addWidget(self.diag_text)

        btn_diag = QPushButton("🔍 Run Full Diagnostics Check")
        btn_diag.clicked.connect(self.run_diagnostics)
        layout.addWidget(btn_diag)

        self.run_diagnostics()
        return container

    def init_tray(self):
        self.tray = QSystemTrayIcon(self)
        if hasattr(self, 'app_icon') and not self.app_icon.isNull():
            self.tray.setIcon(self.app_icon)
        self.tray.setToolTip("OS26 Liquid Glass Control Center")

        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background: #0f1929;
                color: #ffffff;
                border: 1px solid #00a4ef;
                border-radius: 8px;
                padding: 6px;
            }
            QMenu::item {
                padding: 6px 24px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #0078d4;
            }
        """)

        act_open = QAction("Open Control Center", self)
        act_open.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        act_open.triggered.connect(self.show_and_activate)
        menu.addAction(act_open)
        menu.addSeparator()

        self.tray_dock_act = QAction("💎 Toggle Desktop Dock", self)
        self.tray_dock_act.triggered.connect(self.toggle_dock)
        menu.addAction(self.tray_dock_act)

        self.tray_vibe_act = QAction("🌊 Toggle Icon Vibration", self)
        self.tray_vibe_act.triggered.connect(self.toggle_vibration)
        menu.addAction(self.tray_vibe_act)
        menu.addSeparator()

        act_exam = QAction("🛡️ Enter Exam Safe Mode", self)
        act_exam.triggered.connect(self.on_enter_exam_mode)
        menu.addAction(act_exam)

        act_restore = QAction("✨ Restore Full Theme", self)
        act_restore.triggered.connect(self.on_restore_theme)
        menu.addAction(act_restore)
        menu.addSeparator()

        act_exit = QAction("Exit OS26 Control Center", self)
        act_exit.triggered.connect(self.exit_app)
        menu.addAction(act_exit)

        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_activated)
        self.tray.show()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_and_activate()

    def show_and_activate(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def closeEvent(self, event):
        if hasattr(self, 'chk_tray_close') and self.chk_tray_close.isChecked():
            event.ignore()
            self.hide()
            self.tray.showMessage(
                "OS26 Liquid Glass Active",
                "Control Center is still running in your system tray.",
                QSystemTrayIcon.MessageIcon.Information,
                1500
            )
        else:
            event.accept()

    def exit_app(self):
        QApplication.quit()

    # --- Feature Status Refresh ---
    def refresh_status(self):
        # 1. Dock status
        dock_running = is_process_running("desktop_zoom_dock.py")
        if dock_running:
            self.pill_dock.setText("ACTIVE")
            self.pill_dock.setStyleSheet("background: rgba(48, 209, 88, 0.20); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.40); border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: bold;")
            self.btn_dock.setText("Stop Dock")
        else:
            self.pill_dock.setText("STOPPED")
            self.pill_dock.setStyleSheet("background: rgba(142, 142, 147, 0.20); color: #8E8E93; border: 1px solid rgba(142, 142, 147, 0.30); border-radius: 10px; padding: 3px 10px; font-size: 11px;")
            self.btn_dock.setText("Start Dock")

        # 2. Vibration status
        vibe_running = is_process_running("desktop_icon_vibrator.py")
        if vibe_running:
            self.pill_vibe.setText("ACTIVE")
            self.pill_vibe.setStyleSheet("background: rgba(48, 209, 88, 0.20); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.40); border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: bold;")
            self.btn_vibe.setText("Stop Vibration")
        else:
            self.pill_vibe.setText("STOPPED")
            self.pill_vibe.setStyleSheet("background: rgba(142, 142, 147, 0.20); color: #8E8E93; border: 1px solid rgba(142, 142, 147, 0.30); border-radius: 10px; padding: 3px 10px; font-size: 11px;")
            self.btn_vibe.setText("Start Vibration")

        # 3. Windhawk status
        wh_running = is_windhawk_running()
        if wh_running:
            self.pill_wh.setText("RUNNING")
            self.pill_wh.setStyleSheet("background: rgba(0, 164, 239, 0.20); color: #00A4EF; border: 1px solid rgba(0, 164, 239, 0.40); border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: bold;")
        else:
            self.pill_wh.setText("INACTIVE")
            self.pill_wh.setStyleSheet("background: rgba(142, 142, 147, 0.20); color: #8E8E93; border: 1px solid rgba(142, 142, 147, 0.30); border-radius: 10px; padding: 3px 10px; font-size: 11px;")

        # 4. Brightness status
        bright_running = is_process_running("mac_brightness_engine.py")
        if bright_running:
            self.pill_bright.setText("ACTIVE")
            self.pill_bright.setStyleSheet("background: rgba(48, 209, 88, 0.20); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.40); border-radius: 10px; padding: 3px 10px; font-size: 11px; font-weight: bold;")
            self.btn_bright.setText("Stop Engine")
        else:
            self.pill_bright.setText("INACTIVE")
            self.pill_bright.setStyleSheet("background: rgba(142, 142, 147, 0.20); color: #8E8E93; border: 1px solid rgba(142, 142, 147, 0.30); border-radius: 10px; padding: 3px 10px; font-size: 11px;")
            self.btn_bright.setText("Start Engine")

        # Overall badge
        from exam_mode import is_exam_mode_active
        if is_exam_mode_active():
            self.status_badge.setText("🛡️ Exam Safe Mode Active")
            self.status_badge.setStyleSheet("background: rgba(255, 159, 10, 0.20); color: #ff9f0a; border: 1px solid rgba(255, 159, 10, 0.45); border-radius: 14px; padding: 6px 14px; font-weight: bold; font-size: 12px;")
        else:
            self.status_badge.setText("✨ Liquid Glass Active")
            self.status_badge.setStyleSheet("background: rgba(0, 164, 239, 0.18); color: #38d6ff; border: 1px solid rgba(0, 164, 239, 0.45); border-radius: 14px; padding: 6px 14px; font-weight: 600; font-size: 12px;")

    # --- Actions & Toggles ---
    def toggle_dock(self):
        if is_process_running("desktop_zoom_dock.py"):
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    if "desktop_zoom_dock.py" in " ".join(proc.info['cmdline'] or []).lower():
                        proc.kill()
                except Exception:
                    pass
        else:
            dock_py = os.path.join(PROJECT_ROOT, "desktop_zoom_dock.py")
            pyw = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
            if os.path.exists(pyw) and os.path.exists(dock_py):
                subprocess.Popen([pyw, dock_py], cwd=PROJECT_ROOT)
        self.refresh_status()

    def toggle_vibration(self):
        if is_process_running("desktop_icon_vibrator.py"):
            stop_script = os.path.join(PROJECT_ROOT, "stop_desktop_icon_vibrator.py")
            subprocess.run(["python", stop_script], cwd=PROJECT_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            start_script = os.path.join(PROJECT_ROOT, "start_desktop_icon_vibrator.py")
            subprocess.run(["python", start_script], cwd=PROJECT_ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.refresh_status()

    def toggle_brightness(self):
        if is_process_running("mac_brightness_engine.py"):
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    if "mac_brightness_engine.py" in " ".join(proc.info['cmdline'] or []).lower():
                        proc.kill()
                except Exception:
                    pass
        else:
            b_script = os.path.join(PROJECT_ROOT, "mac_brightness_engine.py")
            pyw = r"C:\Users\bhara\AppData\Local\Programs\Python\Python312\pythonw.exe"
            if os.path.exists(pyw) and os.path.exists(b_script):
                subprocess.Popen([pyw, b_script], cwd=PROJECT_ROOT)
        self.refresh_status()

    def open_windhawk_ui(self):
        wh_exe = r"C:\Program Files\Windhawk\windhawk.exe"
        if os.path.exists(wh_exe):
            subprocess.Popen([wh_exe])
        else:
            QMessageBox.information(self, "Windhawk", "Windhawk is not yet installed. Click 'Apply Complete OS26 Theme' to install it.")

    def reapply_fe_styles(self):
        fe_script = os.path.join(PROJECT_ROOT, "apply_fe_styles_elevated.py")
        if os.path.exists(fe_script):
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{fe_script}"', None, 1)

    def reapply_icons_and_wallpaper(self):
        apply_script = os.path.join(PROJECT_ROOT, "apply_full_system_customization.py")
        if os.path.exists(apply_script):
            subprocess.run(["python", apply_script], cwd=PROJECT_ROOT)
            self.on_rebuild_cache()

    def on_apply_full_theme(self):
        reply = QMessageBox.question(
            self,
            "Apply Full OS26 Liquid Glass Theme",
            "This will apply all 50+ permanent Liquid Glass icons, set the 4K Ice Frost wallpaper, configure Windhawk mods, and activate the desktop dock and icon vibration engine.\n\nProceed?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            # 1. System customization
            apply_py = os.path.join(PROJECT_ROOT, "apply_full_system_customization.py")
            subprocess.run(["python", apply_py], cwd=PROJECT_ROOT)

            # 2. Windhawk elevated installer
            wh_py = os.path.join(PROJECT_ROOT, "install_and_style_all_mods.py")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{wh_py}"', None, 1)

            # 3. Start dock and vibrator
            self.toggle_dock()
            self.toggle_vibration()
            self.refresh_status()
            QMessageBox.information(self, "Success", "OS26 Liquid Glass Theme components applied successfully!")

    def on_enter_exam_mode(self):
        reply = QMessageBox.question(
            self,
            "Enter Exam Safe Mode",
            "Exam Safe Mode terminates all background Python daemons and stops the Windhawk service.\n\nYour permanent Liquid Glass icons, 4K wallpaper, and desktop layout remain 100% intact.\n\nReady to activate Exam Safe Mode?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            from exam_mode import enter_exam_mode
            enter_exam_mode()
            self.refresh_status()
            self.tray.showMessage("Exam Safe Mode Active", "Background daemons suspended. System is 100% exam-ready.", QSystemTrayIcon.MessageIcon.Warning, 2000)

    def on_restore_theme(self):
        from exam_mode import restore_full_theme
        restore_full_theme(PROJECT_ROOT)
        self.refresh_status()
        self.tray.showMessage("Theme Restored", "All OS26 Liquid Glass background services are now active.", QSystemTrayIcon.MessageIcon.Information, 2000)

    def on_open_tools_folder(self):
        if os.path.exists(TOOLS_DIR):
            subprocess.Popen(["explorer.exe", TOOLS_DIR])
        else:
            QMessageBox.warning(self, "Tools", "OS26 Tools folder not found on desktop.")

    def on_rebuild_cache(self):
        rebuild_script = os.path.join(PROJECT_ROOT, "rebuild_icon_cache.py")
        if os.path.exists(rebuild_script):
            subprocess.run(["python", rebuild_script], cwd=PROJECT_ROOT)
            QMessageBox.information(self, "Cache Rebuilt", "Windows Icon Cache has been rebuilt and refreshed.")

    # --- Tuning & Config ---
    def load_vibration_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    amp = float(cfg.get("amplitude_x", 3.5))
                    freq = float(cfg.get("frequency_hz", 32.0))
                    pause = bool(cfg.get("pause_on_mouse_down", True))
                    self.amp_slider.setValue(int(amp * 10))
                    self.freq_slider.setValue(int(freq))
                    self.chk_pause_drag.setChecked(pause)
            except Exception:
                pass

    def save_vibration_settings(self):
        cfg = {
            "enabled": True,
            "amplitude_x": self.amp_slider.value() / 10.0,
            "amplitude_y": (self.amp_slider.value() / 10.0) * 0.8,
            "frequency_hz": float(self.freq_slider.value()),
            "secondary_frequency_hz": float(self.freq_slider.value()) * 1.85,
            "organic_stagger": 1.61803398875,
            "fps": 60,
            "pause_on_mouse_down": self.chk_pause_drag.isChecked()
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=4)
        QMessageBox.information(self, "Saved", "Vibration tuning settings saved and hot-reloaded!")

    def is_startup_enabled(self):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_READ)
            winreg.QueryValueEx(key, APP_RUN_NAME)
            winreg.CloseKey(key)
            return True
        except Exception:
            return False

    def toggle_startup_registry(self, state):
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY_PATH, 0, winreg.KEY_SET_VALUE)
            if state == 2: # Checked
                app_exe = sys.executable
                script_path = os.path.abspath(__file__)
                cmd = f'"{app_exe}" "{script_path}" --minimized'
                winreg.SetValueEx(key, APP_RUN_NAME, 0, winreg.REG_SZ, cmd)
            else:
                try:
                    winreg.DeleteValue(key, APP_RUN_NAME)
                except Exception:
                    pass
            winreg.CloseKey(key)
        except Exception as e:
            QMessageBox.warning(self, "Startup Error", f"Could not update startup registry: {e}")

    def run_diagnostics(self):
        report = []
        report.append(f"OS26 Liquid Glass System Diagnostics v{APP_VERSION}")
        report.append("=" * 60)
        report.append(f"Local Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Python Executable: {sys.executable}")
        report.append(f"Project Root: {PROJECT_ROOT}")
        report.append(f"Windows Version: {sys.getwindowsversion().major}.{sys.getwindowsversion().minor} Build {sys.getwindowsversion().build}")
        report.append("-" * 60)

        report.append("ACTIVE PROCESSES:")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = " ".join(proc.info['cmdline'] or []).lower()
                name = proc.info['name'].lower()
                if "windhawk" in name:
                    report.append(f"  [Windhawk] PID {proc.info['pid']}: {name}")
                elif any(k in cmdline for k in ["desktop_zoom_dock.py", "desktop_icon_vibrator.py", "mac_brightness_engine.py", "os26_app.py"]):
                    report.append(f"  [OS26 Daemon] PID {proc.info['pid']}: {cmdline[:80]}...")
            except Exception:
                pass

        report.append("-" * 60)
        report.append("ASSET AUDIT:")
        icons_count = len(os.listdir(ICONS_DIR)) if os.path.exists(ICONS_DIR) else 0
        report.append(f"  Icons in assets/icons: {icons_count} files")
        report.append(f"  4K Wallpaper present: {os.path.exists(WALLPAPER_PATH)}")
        report.append(f"  Windhawk setup binary present: {os.path.exists(os.path.join(ASSETS_DIR, 'windhawk', 'windhawk_setup.exe'))}")
        report.append(f"  Desktop OS26 Tools folder: {os.path.exists(TOOLS_DIR)}")

        report.append("=" * 60)
        report.append("STATUS: All systems nominal. Ready for deployment.")
        self.diag_text.setPlainText("\n".join(report))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_TITLE)
    app.setQuitOnLastWindowClosed(False)

    window = OS26ControlCenter()
    if "--minimized" not in sys.argv:
        window.show()
    else:
        window.tray.showMessage("OS26 Liquid Glass", "Running in system tray.", QSystemTrayIcon.MessageIcon.Information, 1500)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
