import os
import sys
import re
import glob
import math
import subprocess
from PyQt6.QtCore import Qt, QTimer, QRectF, QPointF, QSize, QFileInfo
from PyQt6.QtWidgets import QApplication, QWidget, QMenu, QFileIconProvider
from PyQt6.QtGui import (
    QPainter, QColor, QLinearGradient, QPen, QBrush, QFont,
    QPixmap, QIcon, QPainterPath
)
from PyQt6.QtNetwork import QLocalServer, QLocalSocket

IPC_SERVER_NAME = "OS26_Liquid_Glass_Desktop_Dock_IPC_SingleInstance"


def normalize_str(s):
    """Normalize string to lowercase alphanumeric only for 100% exact matching."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


class DockItem:
    def __init__(self, name, path, icon_path, icon_provider):
        self.name = name
        self.path = path
        self.icon_path = icon_path
        self.pixmap = None
        self.scale = 1.0
        self.target_scale = 1.0
        self.load_icon(icon_provider)

    def load_icon(self, icon_provider):
        if self.icon_path and os.path.exists(self.icon_path):
            ico = QIcon(self.icon_path)
            self.pixmap = ico.pixmap(128, 128)
        
        # Authentic system icon extraction fallback
        if not self.pixmap or self.pixmap.isNull():
            system_icon = icon_provider.icon(QFileInfo(self.path))
            if not system_icon.isNull():
                self.pixmap = system_icon.pixmap(128, 128)

        # Generic safe fallback
        if not self.pixmap or self.pixmap.isNull():
            self.pixmap = QPixmap(128, 128)
            self.pixmap.fill(QColor(120, 160, 240, 220))


class DesktopZoomDock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnBottomHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setMouseTracking(True)

        self.base_icon_size = 48.0
        self.max_scale = 1.50  # Zooms single hovered icon up to ~72px
        self.padding_x = 20.0
        self.padding_y = 10.0
        self.spacing = 8.0
        self.hovered_index = -1
        self.locked_to_bottom = True
        self.always_on_top = False

        self.icon_provider = QFileIconProvider()
        self.items = []
        self.load_desktop_shortcuts()

        # IPC Server to enforce single instance and handle 3-finger tap toggle
        self.setup_ipc_server()

        # Animation loop (60 FPS)
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(16)

        # Lock to bottom initially
        self.recalculate_geometry()

    def setup_ipc_server(self):
        self.ipc_server = QLocalServer(self)
        # Remove any lingering stale socket file
        QLocalServer.removeServer(IPC_SERVER_NAME)
        self.ipc_server.listen(IPC_SERVER_NAME)
        self.ipc_server.newConnection.connect(self.handle_incoming_connection)

    def handle_incoming_connection(self):
        client = self.ipc_server.nextPendingConnection()
        if client:
            client.waitForReadyRead(300)
            msg = client.readAll().data().decode("utf-8", errors="ignore").strip()
            client.disconnectFromServer()
            
            # Always ensure the single instance is visible, raised, and firmly locked at the bottom
            self.show()
            self.recalculate_geometry()
            self.raise_()
            self.activateWindow()

    def load_desktop_shortcuts(self):
        self.items.clear()
        desktop = os.path.expanduser(r"~\OneDrive\Desktop")
        if not os.path.exists(desktop):
            desktop = os.path.expanduser(r"~\Desktop")
        
        icons_dir = r"C:\Users\bhara\AppData\Local\OS26_Liquid_Glass\Icons_Shining"
        available_icons = {}
        if os.path.exists(icons_dir):
            for f in os.listdir(icons_dir):
                if f.endswith(".ico"):
                    norm = normalize_str(f[:-4])
                    # Never use folder icons as generic fallback for app shortcuts
                    if norm not in ("folderclosed", "folderopen"):
                        available_icons[norm] = os.path.join(icons_dir, f)

        shortcuts = glob.glob(os.path.join(desktop, "*.lnk"))
        for sc in sorted(shortcuts):
            raw_name = os.path.splitext(os.path.basename(sc))[0]
            # Don't show the dock shortcut itself inside the dock
            if "Liquid Glass Dock" in raw_name or "desktop_dock" in raw_name.lower():
                continue
                
            norm_name = normalize_str(raw_name)
            matched_icon = None

            # 1. Exact normalized match
            if norm_name in available_icons:
                matched_icon = available_icons[norm_name]
            else:
                # 2. Substring match for versioned names (e.g. pycharm202612 vs pycharm)
                for k, icon_path in available_icons.items():
                    if k in norm_name or norm_name in k:
                        matched_icon = icon_path
                        break

            self.items.append(DockItem(raw_name, sc, matched_icon, self.icon_provider))

    def recalculate_geometry(self):
        # Calculate dock dimensions
        total_items_width = 0.0
        for item in self.items:
            total_items_width += (self.base_icon_size * item.scale) + self.spacing
        if self.items:
            total_items_width -= self.spacing

        total_width = total_items_width + (self.padding_x * 2)
        total_height = (self.base_icon_size * self.max_scale) + (self.padding_y * 2) + 32.0

        new_w = int(math.ceil(total_width))
        new_h = int(math.ceil(total_height))

        # FIRMLY LOCK TO BOTTOM OF SCREEN / WORKSPACE
        screen = QApplication.primaryScreen().availableGeometry()
        x = screen.left() + (screen.width() - new_w) // 2
        # Position anchored right along the bottom of the workspace (above the taskbar)
        y = screen.bottom() - new_h + 2

        self.setGeometry(x, y, new_w, new_h)

    def update_animation(self):
        needs_repaint = False
        for idx, item in enumerate(self.items):
            # As requested: ONLY the specific hovered icon grows
            if idx == self.hovered_index:
                item.target_scale = self.max_scale
            else:
                item.target_scale = 1.0

            diff = item.target_scale - item.scale
            if abs(diff) > 0.002:
                item.scale += diff * 0.28
                needs_repaint = True
            else:
                item.scale = item.target_scale

        if needs_repaint:
            self.recalculate_geometry()
            self.update()

    def mouseMoveEvent(self, event):
        pos = event.position()
        new_hovered = -1
        current_x = self.padding_x

        for idx, item in enumerate(self.items):
            item_size = self.base_icon_size * item.scale
            center_y = self.height() - self.padding_y - (item_size / 2.0)
            
            rect = QRectF(current_x, center_y - (item_size / 2.0), item_size, item_size)
            if rect.contains(pos):
                new_hovered = idx
                break
            current_x += item_size + self.spacing

        if new_hovered != self.hovered_index:
            self.hovered_index = new_hovered
            self.update()

    def leaveEvent(self, event):
        self.hovered_index = -1
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.hovered_index != -1 and self.hovered_index < len(self.items):
                target_item = self.items[self.hovered_index]
                try:
                    os.startfile(target_item.path)
                except Exception as e:
                    print("Error launching:", e)
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_context_menu(event.globalPosition().toPoint())

    def show_context_menu(self, global_pos):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(20, 20, 28, 240);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                padding: 6px;
                font-family: 'Segoe UI Variable Display', 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QMenu::item {
                padding: 6px 20px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background-color: rgba(255, 255, 255, 0.25);
                color: #FFFFFF;
            }
        """)

        lock_action = menu.addAction("Locked to Bottom (Default)")
        lock_action.setCheckable(True)
        lock_action.setChecked(self.locked_to_bottom)
        lock_action.setEnabled(False)  # Permanently locked to bottom

        top_action = menu.addAction("Always On Top" if not self.always_on_top else "Desktop Mode (Behind Windows)")
        reload_action = menu.addAction("Refresh Desktop Shortcuts")
        menu.addSeparator()
        quit_action = menu.addAction("Close Dock")

        action = menu.exec(global_pos)
        if action == top_action:
            self.always_on_top = not self.always_on_top
            self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, self.always_on_top)
            self.show()
            self.recalculate_geometry()
        elif action == reload_action:
            self.load_desktop_shortcuts()
            self.recalculate_geometry()
            self.update()
        elif action == quit_action:
            QApplication.quit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)

        # 1. Draw Liquid Glass Dock Tray
        tray_h = self.base_icon_size + (self.padding_y * 2) - 4.0
        tray_y = self.height() - tray_h
        tray_rect = QRectF(4.0, tray_y, self.width() - 8.0, tray_h)
        tray_radius = tray_h / 2.0

        # Sleek glass gradient
        tray_grad = QLinearGradient(0, tray_y, 0, tray_y + tray_h)
        tray_grad.setColorAt(0.0, QColor(255, 255, 255, 45))
        tray_grad.setColorAt(0.4, QColor(25, 25, 30, 180))
        tray_grad.setColorAt(1.0, QColor(10, 10, 15, 220))
        painter.setBrush(QBrush(tray_grad))

        # Radiant white glass stroke
        tray_border = QLinearGradient(0, tray_y, self.width(), tray_y + tray_h)
        tray_border.setColorAt(0.0, QColor(255, 255, 255, 190))
        tray_border.setColorAt(0.5, QColor(255, 255, 255, 70))
        tray_border.setColorAt(1.0, QColor(255, 255, 255, 160))
        painter.setPen(QPen(QBrush(tray_border), 1.4))
        painter.drawRoundedRect(tray_rect, tray_radius, tray_radius)

        # 2. Draw Icons & Specific Hover Highlight
        current_x = self.padding_x
        hovered_item_for_label = None
        hovered_center_x = 0.0

        for idx, item in enumerate(self.items):
            item_size = self.base_icon_size * item.scale
            center_x = current_x + (item_size / 2.0)
            center_y = self.height() - self.padding_y - (item_size / 2.0)

            # Specific hover highlight: luminous frosted cushion
            if item.scale > 1.04:
                cushion_pad = 7.0 * (item.scale - 1.0) / (self.max_scale - 1.0)
                cushion_rect = QRectF(
                    current_x - cushion_pad,
                    center_y - (item_size / 2.0) - cushion_pad,
                    item_size + (cushion_pad * 2),
                    item_size + (cushion_pad * 2)
                )
                c_radius = 16.0 * item.scale / self.max_scale

                # Radiant white highlight
                hl_grad = QLinearGradient(
                    cushion_rect.left(), cushion_rect.top(),
                    cushion_rect.right(), cushion_rect.bottom()
                )
                hl_grad.setColorAt(0.0, QColor(255, 255, 255, 100))
                hl_grad.setColorAt(1.0, QColor(255, 255, 255, 35))
                painter.setBrush(QBrush(hl_grad))
                painter.setPen(QPen(QColor(255, 255, 255, 240), 2.0))
                painter.drawRoundedRect(cushion_rect, c_radius, c_radius)

            # Draw the app icon
            icon_rect = QRectF(
                current_x,
                center_y - (item_size / 2.0),
                item_size,
                item_size
            )
            if item.pixmap:
                painter.drawPixmap(icon_rect.toRect(), item.pixmap)

            if idx == self.hovered_index:
                hovered_item_for_label = item
                hovered_center_x = center_x

            current_x += item_size + self.spacing

        # 3. Floating Tooltip Label
        if hovered_item_for_label:
            font = QFont("Segoe UI Variable Display", 10)
            font.setBold(True)
            painter.setFont(font)

            label_text = hovered_item_for_label.name
            metrics = painter.fontMetrics()
            text_w = metrics.horizontalAdvance(label_text)
            text_h = metrics.height()

            label_pad_x = 12.0
            label_pad_y = 5.0
            label_rect = QRectF(
                hovered_center_x - (text_w / 2.0) - label_pad_x,
                8.0,
                text_w + (label_pad_x * 2.0),
                text_h + (label_pad_y * 2.0)
            )

            # Glass label container
            label_grad = QLinearGradient(label_rect.left(), label_rect.top(), label_rect.right(), label_rect.bottom())
            label_grad.setColorAt(0.0, QColor(25, 25, 35, 230))
            label_grad.setColorAt(1.0, QColor(15, 15, 20, 245))
            painter.setBrush(QBrush(label_grad))
            painter.setPen(QPen(QColor(255, 255, 255, 170), 1.2))
            painter.drawRoundedRect(label_rect, 10.0, 10.0)

            # Text
            painter.setPen(QColor(255, 255, 255, 255))
            painter.drawText(label_rect, Qt.AlignmentFlag.AlignCenter, label_text)


def main():
    app = QApplication(sys.argv)

    # -------------------------------------------------------------
    # STRICT SINGLE-INSTANCE CHECK
    # -------------------------------------------------------------
    socket = QLocalSocket()
    socket.connectToServer(IPC_SERVER_NAME)
    if socket.waitForConnected(400):
        # Already running! Send toggle signal to show/hide the existing dock and exit immediately!
        socket.write(b"toggle")
        socket.waitForBytesWritten(400)
        socket.disconnectFromServer()
        sys.exit(0)

    # Primary instance
    dock = DesktopZoomDock()
    dock.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
