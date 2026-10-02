import os
import sys
import time
from PyQt6.QtCore import Qt, QTimer, QRect
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor
import win32com.client

class BlackoutScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.hide()

    def update_geometry_to_all_screens(self):
        total_rect = QRect()
        for screen in QApplication.screens():
            total_rect = total_rect.united(screen.geometry())
        self.setGeometry(total_rect)

    def paintEvent(self, event):
        painter = QPainter(self)
        # 100% Solid Pitch Black (MacBook / Linux 0 nits style)
        painter.fillRect(self.rect(), QColor(0, 0, 0))

    def keyPressEvent(self, event):
        # Emergency exit if user presses Esc or Space
        if event.key() in (Qt.Key.Key_Escape, Qt.Key.Key_Space):
            self.hide()
        super().keyPressEvent(event)


class BrightnessManager:
    def __init__(self, blackout_widget):
        self.blackout = blackout_widget
        self.last_brightness = -1
        self.wmi = None
        self.init_wmi()

    def init_wmi(self):
        try:
            self.wmi = win32com.client.GetObject(r"winmgmts:\\.\root\wmi")
        except Exception as e:
            print("WMI init error:", e)

    def check_brightness(self):
        try:
            if not self.wmi:
                self.init_wmi()
                if not self.wmi:
                    return

            instances = self.wmi.InstancesOf("WmiMonitorBrightness")
            for inst in instances:
                b = int(inst.CurrentBrightness)
                if b != self.last_brightness:
                    self.last_brightness = b
                    self.on_brightness_changed(b)
                break
        except Exception:
            # Re-init WMI if handle broke
            self.wmi = None

    def on_brightness_changed(self, brightness):
        # When brightness is 0: Full Black Screen (MacBook / Linux style)
        if brightness == 0:
            if not self.blackout.isVisible():
                self.blackout.update_geometry_to_all_screens()
                self.blackout.showFullScreen()
                self.blackout.raise_()
        else:
            # When brightness is 1-100: Screen is fully visible and bright
            if self.blackout.isVisible():
                self.blackout.hide()


def main():
    app = QApplication(sys.argv)
    blackout = BlackoutScreen()
    manager = BrightnessManager(blackout)

    # Check brightness every 100ms for instant response to keys / slider
    timer = QTimer()
    timer.timeout.connect(manager.check_brightness)
    timer.start(100)

    # Initial check
    manager.check_brightness()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
