from PyQt5.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLabel, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont

def create_styled_button():
    start_btn = QPushButton("Start")
    start_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.2), 
                stop:0.3 rgba(255, 255, 255, 0.15),
                stop:0.7 rgba(255, 255, 255, 0.1),
                stop:1 rgba(255, 255, 255, 0.05));
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: "Segoe UI", Arial, sans-serif;
            padding: 15px 30px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            border-radius: 25px;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.3), 
                stop:0.3 rgba(255, 255, 255, 0.25),
                stop:0.7 rgba(255, 255, 255, 0.2),
                stop:1 rgba(255, 255, 255, 0.15));
            border: 1px solid rgba(255, 255, 255, 0.6);
        }
        QPushButton:pressed {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.25), 
                stop:0.3 rgba(255, 255, 255, 0.2),
                stop:0.7 rgba(255, 255, 255, 0.15),
                stop:1 rgba(255, 255, 255, 0.1));
            border: 1px solid rgba(255, 255, 255, 0.8);
        }
    """)

    # Outer glow effect (replaces box-shadow)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(20)
    shadow.setColor(QColor(255, 255, 255, 80))
    shadow.setOffset(0, 0)
    start_btn.setGraphicsEffect(shadow)
    
    start_btn.setFixedSize(200, 60)
    return start_btn

class HomePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(180)
        layout.setContentsMargins(50, 0, 50, 0)
        
        # Title
        title = QLabel("MotionMate")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 85px;
                font-weight: bold;
                font-family: "Segoe UI", Arial, sans-serif;
                padding: 0px;
                margin: 0px;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Button
        self.start_btn = create_styled_button()
        self.start_btn.clicked.connect(self.go_to_options)
        
        # Add to layout with stretches to center everything
        layout.addStretch(1)
        layout.addWidget(title)
        layout.addWidget(self.start_btn, 0, Qt.AlignCenter)
        layout.addStretch(1)
        
        self.setLayout(layout)
    
    def go_to_options(self):
        # Get the main app instance and navigate to options page
        main_app = self.parent()  # This is the MotionMimicApp (QStackedWidget)
        if main_app:
            # Since we know OptionsPage is at index 1 (second page)
            if main_app.count() > 2:
                main_app.setCurrentIndex(1)
            else:
                print("Config page not found - available pages:", main_app.count())