"""
OS26 Liquid Glass - Face ID Enrollment Studio
Uses OpenCV and the built-in HP Wide Vision HD Camera to capture,
encode, and train an authentic facial recognition biometric model.
"""

import os
import sys
import json
import time
import cv2
import numpy as np
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QProgressBar, QFrame, QMessageBox, QLineEdit
)
from PyQt6.QtGui import QImage, QPixmap, QFont, QColor, QPainter, QPen, QBrush

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "face_data")
os.makedirs(DATA_DIR, exist_ok=True)

MODEL_PATH = os.path.join(DATA_DIR, "face_model.yml")
CONFIG_PATH = os.path.join(DATA_DIR, "face_config.json")
CASCADE_PATH = os.path.join(PROJECT_ROOT, "haarcascade_frontalface_default.xml")
if not os.path.exists(CASCADE_PATH):
    CASCADE_PATH = os.path.join(SCRIPT_DIR, "haarcascade_frontalface_default.xml")

class FaceEnrollWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OS26 Face ID Enrollment Studio")
        self.resize(700, 720)
        self.setMinimumSize(650, 680)

        self.cap = None
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        self.captured_faces = []
        self.enrolling = False
        self.target_samples = 35

        self.setup_ui()
        self.start_camera()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #090e17, stop:0.5 #0d1522, stop:1 #060a11);
                color: #ffffff;
                font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #e6edf8;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0078d4, stop:1 #005a9e);
                border: 1px solid #33bbf5;
                border-radius: 10px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0086ed, stop:1 #0066b3);
                border: 1px solid #66ccff;
            }
            QLineEdit {
                background: rgba(18, 28, 45, 0.85);
                border: 1px solid rgba(0, 164, 239, 0.40);
                border-radius: 8px;
                color: #ffffff;
                font-size: 14px;
                padding: 8px 12px;
            }
            QProgressBar {
                background: rgba(18, 28, 45, 0.80);
                border: 1px solid rgba(255, 255, 255, 0.10);
                border-radius: 8px;
                height: 14px;
                text-align: center;
                font-size: 11px;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #0078d4, stop:1 #00c3ff);
                border-radius: 7px;
            }
        """)

        widget = QWidget()
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(30, 24, 30, 24)
        layout.setSpacing(14)

        # Title
        title_box = QVBoxLayout()
        title = QLabel("✨ Set Up Face ID Authentication")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_box.addWidget(title)

        subtitle = QLabel("Look into your camera. We will map your facial features for instant login.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setStyleSheet("color: #79d2ff;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_box.addWidget(subtitle)
        layout.addLayout(title_box)

        # Camera Display Frame
        cam_frame = QFrame()
        cam_frame.setStyleSheet("""
            background: #05080f;
            border: 2px solid rgba(0, 164, 239, 0.35);
            border-radius: 16px;
        """)
        cam_layout = QVBoxLayout(cam_frame)
        cam_layout.setContentsMargins(8, 8, 8, 8)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setMinimumSize(480, 360)
        cam_layout.addWidget(self.video_label)
        layout.addWidget(cam_frame)

        # Status text
        self.status_label = QLabel("Camera active. Align your face inside the frame.")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #a8bfde; font-size: 13px; font-weight: 500;")
        layout.addWidget(self.status_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # User Name and PIN Inputs
        input_row = QHBoxLayout()
        name_lbl = QLabel("User Name:")
        name_lbl.setStyleSheet("font-weight: 600;")
        self.name_input = QLineEdit("Bharath")
        pin_lbl = QLabel("Backup PIN:")
        pin_lbl.setStyleSheet("font-weight: 600;")
        self.pin_input = QLineEdit("1234")
        self.pin_input.setMaximumWidth(90)
        self.pin_input.setPlaceholderText("PIN")

        input_row.addWidget(name_lbl)
        input_row.addWidget(self.name_input)
        input_row.addSpacing(16)
        input_row.addWidget(pin_lbl)
        input_row.addWidget(self.pin_input)
        layout.addLayout(input_row)

        # Action Button
        self.enroll_btn = QPushButton("📸 Start Face Enrollment")
        self.enroll_btn.clicked.connect(self.start_enrollment)
        layout.addWidget(self.enroll_btn)

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30) # ~33 FPS

    def update_frame(self):
        if not self.cap or not self.cap.isOpened():
            return
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip horizontally for natural mirror feel
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(90, 90))

        # Draw HUD overlays on frame
        for (x, y, fw, fh) in faces:
            # Rounded corner HUD box
            color = (0, 220, 255) if not self.enrolling else (0, 255, 120)
            cv2.rectangle(frame, (x, y), (x + fw, y + fh), color, 2)
            cv2.putText(frame, "Face ID Scanner", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)

            if self.enrolling:
                # Capture face crop
                face_crop = gray[y:y+fh, x:x+fw]
                face_resized = cv2.resize(face_crop, (200, 200))
                self.captured_faces.append(face_resized)

                # Save first sample as avatar
                if len(self.captured_faces) == 1:
                    avatar_path = os.path.join(DATA_DIR, "avatar.jpg")
                    cv2.imwrite(avatar_path, frame[y:y+fh, x:x+fw])

                count = len(self.captured_faces)
                pct = int((count / self.target_samples) * 100)
                self.progress_bar.setValue(pct)
                self.status_label.setText(f"Scanning facial biometric points... ({count}/{self.target_samples})")

                if count >= self.target_samples:
                    self.finish_enrollment()
                    break

        # Convert frame to Qt QImage
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bytes_per_line = c * w
        q_img = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pix = QPixmap.fromImage(q_img).scaled(self.video_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.video_label.setPixmap(pix)

    def start_enrollment(self):
        self.captured_faces = []
        self.enrolling = True
        self.progress_bar.setValue(0)
        self.enroll_btn.setEnabled(False)
        self.enroll_btn.setText("Capturing Facial Biometrics...")
        self.status_label.setText("Look steadily at the camera and turn your head very slightly.")

    def finish_enrollment(self):
        self.enrolling = False
        self.timer.stop()
        self.status_label.setText("Training facial biometric model...")
        QApplication.processEvents()

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            labels = np.array([1] * len(self.captured_faces))
            recognizer.train(self.captured_faces, labels)
            recognizer.save(MODEL_PATH)

            config = {
                "user_name": self.name_input.text().strip() or "User",
                "backup_pin": self.pin_input.text().strip() or "1234",
                "threshold": 75.0,
                "enrolled_at": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            with open(CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)

            QMessageBox.information(
                self,
                "Face ID Enrolled!",
                f"Face ID successfully registered for {config['user_name']}!\n\nBackup PIN: {config['backup_pin']}\n\nYou can now test Face Unlock immediately."
            )
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to train face model: {e}")
            self.enroll_btn.setEnabled(True)
            self.enroll_btn.setText("Retry Face Enrollment")
            self.timer.start(30)

    def closeEvent(self, event):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        event.accept()

def main():
    app = QApplication(sys.argv)
    win = FaceEnrollWindow()
    win.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
