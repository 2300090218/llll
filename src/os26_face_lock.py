"""
OS26 Liquid Glass - Face ID Lock Screen & Authentication Engine
Authenticates the user via webcam facial recognition and unlocks the laptop.
Includes animated scanning HUD, PIN fallback, and full OS26 Liquid Glass aesthetics.
"""

import os
import sys
import json
import time
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QTimer, QTime, QDate, QRectF, QPointF
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import (
    QImage, QPixmap, QFont, QColor, QPainter, QPen, QBrush,
    QPainterPath, QLinearGradient
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "face_data")
MODEL_PATH = os.path.join(DATA_DIR, "face_model.yml")
CONFIG_PATH = os.path.join(DATA_DIR, "face_config.json")
CASCADE_PATH = os.path.join(PROJECT_ROOT, "haarcascade_frontalface_default.xml")
if not os.path.exists(CASCADE_PATH):
    CASCADE_PATH = os.path.join(SCRIPT_DIR, "haarcascade_frontalface_default.xml")
WALLPAPER_PATH = os.path.join(PROJECT_ROOT, "assets", "wallpaper", "OS26_Ice_Frost_Wallpaper_4K.jpg")
if not os.path.exists(WALLPAPER_PATH):
    WALLPAPER_PATH = os.path.join(PROJECT_ROOT, "OS26_Ice_Frost_Wallpaper_4K.jpg")

class FaceLockScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.showFullScreen()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Load user configuration
        self.user_name = "User"
        self.backup_pin = "1234"
        self.threshold = 75.0
        self.load_config()

        # Load recognizer
        self.recognizer = None
        if os.path.exists(MODEL_PATH):
            try:
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read(MODEL_PATH)
            except Exception as e:
                print("Error loading face model:", e)

        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

        self.cap = cv2.VideoCapture(0)
        self.scan_angle = 0
        self.match_streak = 0
        self.authenticated = False
        self.show_pin_pad = False
        self.status_text = "Looking for your face..."
        self.status_color = QColor(0, 195, 255)

        self.setup_ui()

        # Camera frame timer (30 FPS)
        self.cam_timer = QTimer(self)
        self.cam_timer.timeout.connect(self.process_camera)
        self.cam_timer.start(33)

        # Clock timer (1s)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                    self.user_name = cfg.get("user_name", "Bharath")
                    self.backup_pin = str(cfg.get("backup_pin", "1234"))
                    self.threshold = float(cfg.get("threshold", 75.0))
            except Exception:
                pass

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 50, 40, 40)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Top Bar: Padlock icon + Status
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        self.lock_icon_lbl = QLabel("🔒")
        self.lock_icon_lbl.setFont(QFont("Segoe UI Emoji", 20))
        top_bar.addWidget(self.lock_icon_lbl)
        self.lock_status_lbl = QLabel("Face ID Locked")
        self.lock_status_lbl.setFont(QFont("Segoe UI Variable", 13, QFont.Weight.DemiBold))
        self.lock_status_lbl.setStyleSheet("color: rgba(255, 255, 255, 0.75);")
        top_bar.addWidget(self.lock_status_lbl)
        top_bar.addStretch()
        main_layout.addLayout(top_bar)

        main_layout.addSpacing(20)

        # Clock & Date
        self.time_lbl = QLabel(QTime.currentTime().toString("h:mm AP"))
        self.time_lbl.setFont(QFont("Segoe UI Variable Display", 64, QFont.Weight.DemiBold))
        self.time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_lbl.setStyleSheet("color: #ffffff; letter-spacing: 1px;")
        main_layout.addWidget(self.time_lbl)

        self.date_lbl = QLabel(QDate.currentDate().toString("dddd, MMMM d"))
        self.date_lbl.setFont(QFont("Segoe UI Variable", 16))
        self.date_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_lbl.setStyleSheet("color: #a8bfde;")
        main_layout.addWidget(self.date_lbl)

        main_layout.addSpacing(35)

        # Face ID Camera Radar Display
        self.radar_frame = QFrame()
        self.radar_frame.setFixedSize(220, 220)
        self.radar_frame.setStyleSheet("""
            background: rgba(10, 16, 26, 0.65);
            border: 2px solid rgba(0, 195, 255, 0.50);
            border-radius: 110px;
        """)
        rf_layout = QVBoxLayout(self.radar_frame)
        rf_layout.setContentsMargins(6, 6, 6, 6)

        self.cam_preview = QLabel()
        self.cam_preview.setFixedSize(204, 204)
        self.cam_preview.setStyleSheet("border-radius: 102px; background: #05080f;")
        self.cam_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rf_layout.addWidget(self.cam_preview)

        main_layout.addWidget(self.radar_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        # Status text below radar
        self.scan_msg_lbl = QLabel(self.status_text)
        self.scan_msg_lbl.setFont(QFont("Segoe UI Variable", 14, QFont.Weight.Medium))
        self.scan_msg_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scan_msg_lbl.setStyleSheet("color: #00c3ff; margin-top: 12px;")
        main_layout.addWidget(self.scan_msg_lbl)

        # PIN Fallback Area (Hidden initially)
        self.pin_container = QWidget()
        pin_layout = QVBoxLayout(self.pin_container)
        pin_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pin_desc = QLabel(f"Enter PIN for {self.user_name}:")
        pin_desc.setFont(QFont("Segoe UI", 12))
        pin_desc.setStyleSheet("color: #ffffff;")
        pin_layout.addWidget(pin_desc, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pin_input = QLineEdit()
        self.pin_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pin_input.setMaximumWidth(160)
        self.pin_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin_input.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.pin_input.setStyleSheet("""
            background: rgba(18, 28, 45, 0.90);
            border: 2px solid #00a4ef;
            border-radius: 10px;
            color: #ffffff;
            padding: 8px;
        """)
        self.pin_input.textChanged.connect(self.check_pin)
        pin_layout.addWidget(self.pin_input, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pin_container.hide()
        main_layout.addWidget(self.pin_container)

        main_layout.addStretch()

        # Bottom hint
        hint = QLabel("Looking at the screen unlocks automatically • Press any key for PIN • Esc to exit")
        hint.setFont(QFont("Segoe UI", 11))
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setStyleSheet("color: rgba(255, 255, 255, 0.40);")
        main_layout.addWidget(hint)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 1. Draw 4K Wallpaper background
        if os.path.exists(WALLPAPER_PATH):
            wp = QPixmap(WALLPAPER_PATH)
            painter.drawPixmap(self.rect(), wp)
        else:
            painter.fillRect(self.rect(), QColor(9, 14, 23))

        # 2. Draw Frosted Acrylic Glass tint
        glass_tint = QLinearGradient(0, 0, 0, self.height())
        glass_tint.setColorAt(0, QColor(8, 14, 24, 205))
        glass_tint.setColorAt(0.5, QColor(10, 18, 30, 215))
        glass_tint.setColorAt(1, QColor(5, 8, 15, 230))
        painter.fillRect(self.rect(), glass_tint)

    def update_clock(self):
        self.time_lbl.setText(QTime.currentTime().toString("h:mm AP"))
        self.date_lbl.setText(QDate.currentDate().toString("dddd, MMMM d"))

    def process_camera(self):
        if not self.cap or not self.cap.isOpened() or self.authenticated:
            return

        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80))

        if len(faces) > 0 and self.recognizer:
            (x, y, fw, fh) = faces[0]
            face_crop = gray[y:y+fh, x:x+fw]
            face_resized = cv2.resize(face_crop, (200, 200))

            label, confidence = self.recognizer.predict(face_resized)

            # Lower confidence in LBPH means closer distance
            if confidence <= self.threshold:
                self.match_streak += 1
                self.status_text = f"Recognizing {self.user_name}..."
                self.scan_msg_lbl.setText(self.status_text)
                self.scan_msg_lbl.setStyleSheet("color: #30D158; font-weight: bold;")

                if self.match_streak >= 2:
                    self.on_unlock_success()
                    return
            else:
                self.match_streak = 0
                self.status_text = "Face not recognized. Tap screen for PIN."
                self.scan_msg_lbl.setText(self.status_text)
                self.scan_msg_lbl.setStyleSheet("color: #ff9f0a;")
        else:
            self.match_streak = 0
            if not self.show_pin_pad:
                self.status_text = "Looking for your face..."
                self.scan_msg_lbl.setText(self.status_text)
                self.scan_msg_lbl.setStyleSheet("color: #00c3ff;")

        # Circular preview rendering
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bytes_per_line = c * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        # Crop to square center
        min_dim = min(w, h)
        cx, cy = w // 2, h // 2
        square_img = q_img.copy(cx - min_dim // 2, cy - min_dim // 2, min_dim, min_dim)

        # Mask circular
        circular_pix = QPixmap(204, 204)
        circular_pix.fill(Qt.GlobalColor.transparent)
        p = QPainter(circular_pix)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addEllipse(0, 0, 204, 204)
        p.setClipPath(path)
        p.drawPixmap(0, 0, 204, 204, QPixmap.fromImage(square_img))
        p.end()

        self.cam_preview.setPixmap(circular_pix)

    def on_unlock_success(self):
        self.authenticated = True
        self.cam_timer.stop()
        if self.cap and self.cap.isOpened():
            self.cap.release()

        self.lock_icon_lbl.setText("🔓")
        self.lock_status_lbl.setText("Unlocked")
        self.radar_frame.setStyleSheet("background: rgba(48, 209, 88, 0.35); border: 3px solid #30D158; border-radius: 110px;")
        self.scan_msg_lbl.setText(f"✨ Welcome back, {self.user_name}!")
        self.scan_msg_lbl.setStyleSheet("color: #30D158; font-size: 16px; font-weight: bold;")

        QTimer.singleShot(700, self.close)

    def check_pin(self, text):
        if text == self.backup_pin:
            self.on_unlock_success()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()
        elif not self.show_pin_pad:
            self.show_pin_pad = True
            self.radar_frame.hide()
            self.scan_msg_lbl.hide()
            self.pin_container.show()
            self.pin_input.setFocus()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if not self.show_pin_pad:
            self.show_pin_pad = True
            self.radar_frame.hide()
            self.scan_msg_lbl.hide()
            self.pin_container.show()
            self.pin_input.setFocus()
        super().mousePressEvent(event)

    def closeEvent(self, event):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    screen = FaceLockScreen()
    screen.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
