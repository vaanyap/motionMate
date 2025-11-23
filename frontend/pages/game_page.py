import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QTimer
from camera_feed import cv_to_pixmap

class GamePage(QWidget):
    def __init__(self, controller):
        super().__init__()

        # Let the parent background show through
        self.setStyleSheet("background: transparent;")

        self.controller = controller
        self.cap = cv2.VideoCapture(0)

        self.video_label = QLabel()
        self.video_label.setFixedSize(800, 500)

        back_btn = QPushButton("Back")
        back_btn.setStyleSheet("font-size: 20px; padding: 10px;")
        back_btn.clicked.connect(self.go_back)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(back_btn)
        self.setLayout(layout)

        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)   # ~30 FPS

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            pixmap = cv_to_pixmap(frame)
            self.video_label.setPixmap(pixmap)

    def go_back(self):
        self.controller.setCurrentIndex(0)
