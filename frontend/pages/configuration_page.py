import json
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QGroupBox, QScrollArea, QSlider, QSpinBox, QProgressBar,QGridLayout,QFrame,QTextEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette

class ConfigurationPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_step = 0
        self.focus_checks = []
        self.user_data = {}
        self.config_file = "user_profile.json"
        self.setup_ui()
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing user data from JSON file if it exists"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.user_data = json.load(f)
            except:
                self.user_data = {}
        else:
            self.user_data = {}
    
    def save_to_json(self):
        """Save current user data to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving to JSON: {e}")
    
    def update_user_data(self, key, value):
        """Update user data and save to JSON"""
        self.user_data[key] = value
        self.save_to_json()
    
    def toggle_health_condition(self, condition, checked):
        """Add or remove health condition from user data"""
        if 'health_conditions' not in self.user_data:
            self.user_data['health_conditions'] = []
        
        if checked and condition not in self.user_data['health_conditions']:
            self.user_data['health_conditions'].append(condition)
        elif not checked and condition in self.user_data['health_conditions']:
            self.user_data['health_conditions'].remove(condition)
        
        self.save_to_json()
    
    def toggle_body_part(self, body_part, checked):
        """Add or remove body part from user data"""
        if 'body_parts' not in self.user_data:
            self.user_data['body_parts'] = []
        
        if checked and body_part not in self.user_data['body_parts']:
            self.user_data['body_parts'].append(body_part)
        elif not checked and body_part in self.user_data['body_parts']:
            self.user_data['body_parts'].remove(body_part)
        
        self.save_to_json()
    
    def toggle_audio_cues(self, state):
        """Update audio cues setting"""
        self.user_data['audio_cues'] = (state == Qt.Checked)
        self.save_to_json()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Make the main widget transparent
        self.setStyleSheet("background: transparent;")
        
        # Progress bar at top - make semi-transparent
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3b82f6, stop:1 #10b981);
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Scroll area for content - make transparent
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.3);
                border-radius: 4px;
            }
        """)
        
        # Content widget - make transparent
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(30)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        
        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)
        
        # Navigation buttons at bottom - make semi-transparent
        self.nav_widget = QWidget()
        self.nav_widget.setStyleSheet("background: rgba(255, 255, 255, 0.1);")
        self.nav_widget.setFixedHeight(80)
        self.nav_layout = QHBoxLayout(self.nav_widget)
        self.nav_layout.setContentsMargins(40, 0, 40, 0)
        
        # Create container for left buttons - make transparent
        self.left_button_container = QWidget()
        self.left_button_container.setStyleSheet("background: transparent;")
        self.left_button_layout = QHBoxLayout(self.left_button_container)
        self.left_button_layout.setContentsMargins(0, 0, 0, 0)
        self.left_button_layout.setSpacing(10)
        
        # Create both buttons with semi-transparent backgrounds
        self.back_to_home_btn = QPushButton("← Back to Home")
        self.back_to_home_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3), 
                    stop:1 rgba(255, 255, 255, 0.1));
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.4), 
                    stop:1 rgba(255, 255, 255, 0.2));
            }
        """)
        self.back_to_home_btn.clicked.connect(self.go_to_home)
        
        # Regular Back button (for other steps)
        self.back_btn = QPushButton("Back")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 16px;
                padding: 12px 25px;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.2);
            }
        """)
        self.back_btn.clicked.connect(self.previous_step)
        
        self.next_btn = QPushButton("Next")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.3), 
                    stop:1 rgba(255, 255, 255, 0.1));
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 25px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                border-radius: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.4), 
                    stop:1 rgba(255, 255, 255, 0.2));
            }
        """)
        self.next_btn.clicked.connect(self.next_step)
        
        # Build the fixed navigation structure
        self.nav_layout.addWidget(self.left_button_container)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_btn)
        
        layout.addWidget(self.nav_widget)
        self.setLayout(layout)
        
        # Initialize steps
        self.steps = [
            self.create_profile_step,
            self.create_preferences_step,
            self.create_accessibility_step,
            self.create_review_step
        ]
        
        self.update_step()
    
    def update_step(self):
        # Clear current content
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Update progress - convert to integer
        progress = int((self.current_step / (len(self.steps) - 1)) * 100)
        self.progress_bar.setValue(progress)
        
        # Show current step
        self.steps[self.current_step]()
        
        # Update navigation buttons
        self.update_navigation_buttons()
    
    def update_navigation_buttons(self):
        # Clear the left button container
        while self.left_button_layout.count():
            child = self.left_button_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)  # Hide but don't delete
        
        # Add appropriate back button based on current step
        if self.current_step == 0:
            # First step - show "Back to Home"
            self.left_button_layout.addWidget(self.back_to_home_btn)
        else:
            # Other steps - show regular "Back"
            self.left_button_layout.addWidget(self.back_btn)
        
        # Update button states
        if self.current_step == len(self.steps) - 1:
            self.next_btn.setText("Finish")
        else:
            self.next_btn.setText("Next")
    
    def create_profile_step(self):
        # Step title
        title = QLabel("About You")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        subtitle = QLabel("Help us understand your body & health")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            background: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(subtitle)
        
        self.content_layout.addSpacing(40)
        
        # Main two-column layout
        columns_layout = QHBoxLayout()
        columns_layout.setSpacing(30)  # Space between columns
        
        # Left column - Age & Fitness
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        # Age range
        age_group = QGroupBox("Age Range")
        age_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        age_layout = QVBoxLayout()
        
        age_combo = QComboBox()
        age_combo.addItems([
            "Under 18",
            "18-25 (Young Adult)",
            "26-35 (Adult)", 
            "36-45 (Middle Age)",
            "46-60 (Senior)",
            "60+ (Elderly)"
        ])
        age_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                selection-background-color: rgba(59, 130, 246, 0.5);
            }
        """)
        
        # Load existing age selection
        if 'age_range' in self.user_data:
            age_combo.setCurrentText(self.user_data['age_range'])
        
        # Save when selection changes
        age_combo.currentTextChanged.connect(lambda text: self.update_user_data('age_range', text))
        
        age_layout.addWidget(age_combo)
        age_group.setLayout(age_layout)
        left_column.addWidget(age_group)
        
        # Fitness level
        fitness_group = QGroupBox("Fitness Level")
        fitness_group.setStyleSheet(age_group.styleSheet())
        fitness_layout = QVBoxLayout()
        
        fitness_combo = QComboBox()
        fitness_combo.setStyleSheet(age_combo.styleSheet())
        fitness_combo.addItems([
            "Beginner - Just starting out",
            "Intermediate - Regular exercise", 
            "Advanced - Athlete"
        ])
        
        # Load existing fitness selection
        if 'fitness_level' in self.user_data:
            fitness_combo.setCurrentText(self.user_data['fitness_level'])
        
        # Save when selection changes
        fitness_combo.currentTextChanged.connect(lambda text: self.update_user_data('fitness_level', text))
        
        fitness_layout.addWidget(fitness_combo)
        fitness_group.setLayout(fitness_layout)
        left_column.addWidget(fitness_group)
        
        # Add stretch to push content to top in left column
        left_column.addStretch()
        
        # Right column - Health Conditions
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        # Health Conditions
        health_group = QGroupBox("Disabilities")
        health_group.setStyleSheet(age_group.styleSheet())
        health_layout = QVBoxLayout()
        
        health_checks = []
        conditions = ["Parkinson's Disease", "Osteoporosis", "Arthritis", "Pregnancy", "Cardiovascular Issue"]
        
        for condition in conditions:
            check = QCheckBox(condition)
            check.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 16px;
                    spacing: 10px;
                    background: transparent;
                    padding: 5px;
                }
                QCheckBox::indicator {
                    width: 20px;
                    height: 20px;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    border-radius: 4px;
                    background: rgba(255, 255, 255, 0.1);
                }
                QCheckBox::indicator:checked {
                    background: #3b82f6;
                    border: 2px solid #3b82f6;
                }
            """)
            
            # Load existing health condition selections
            if 'health_conditions' in self.user_data and condition in self.user_data['health_conditions']:
                check.setChecked(True)
            
            # Save when toggled
            check.toggled.connect(lambda checked, cond=condition: self.toggle_health_condition(cond, checked))
            
            health_layout.addWidget(check)
            health_checks.append(check)
        
        health_group.setLayout(health_layout)
        right_column.addWidget(health_group)
        
        # Add stretch to push content to top in right column
        right_column.addStretch()
        
        # Add both columns to main layout
        columns_layout.addLayout(left_column)
        columns_layout.addLayout(right_column)
        
        # Make both columns equal width
        columns_layout.setStretchFactor(left_column, 1)
        columns_layout.setStretchFactor(right_column, 1)
        
        self.content_layout.addLayout(columns_layout)
        self.content_layout.addStretch()
    
    def create_preferences_step(self):
        title = QLabel("Exercise Preferences")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        subtitle = QLabel("Further tailor the workout plans to your needs")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            background: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(subtitle)
        
        self.content_layout.addSpacing(40)
        
        # Body parts group
        body_group = QGroupBox("Which parts of your body are affected?")
        body_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Create grid layout with 4 columns
        body_layout = QGridLayout()
        body_layout.setSpacing(15)  # Space between checkboxes
        body_layout.setHorizontalSpacing(30)  # More space between columns
        body_layout.setVerticalSpacing(15)
        
        body_parts = [
            "Whole Body / General",
            "Spine / Back", 
            "Neck",
            "Shoulders",
            "Arms / Hands",
            "Wrists", 
            "Hips",
            "Legs / Knees",
            "Ankles / Feet",
            "Joints (general)",
            "Cardiovascular System / Heart",
            "Balance / Coordination"
        ]
        
        body_checks = []  # Local variable
        
        # Add checkboxes to grid (4 columns)
        for i, body_part in enumerate(body_parts):
            row = i // 4  # Integer division for row
            col = i % 4   # Remainder for column
            
            check = QCheckBox(body_part)
            check.setStyleSheet("""
                QCheckBox {
                    color: white;
                    font-size: 14px;
                    spacing: 8px;
                    background: transparent;
                    padding: 8px 5px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border: 2px solid rgba(255, 255, 255, 0.5);
                    border-radius: 3px;
                    background: rgba(255, 255, 255, 0.1);
                }
                QCheckBox::indicator:checked {
                    background: #3b82f6;
                    border: 2px solid #3b82f6;
                }
                QCheckBox:hover {
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 5px;
                }
            """)
            
            # Load existing body part selections
            if 'body_parts' in self.user_data and body_part in self.user_data['body_parts']:
                check.setChecked(True)
            
            # Save when toggled
            check.toggled.connect(lambda checked, bp=body_part: self.toggle_body_part(bp, checked))
            
            body_layout.addWidget(check, row, col)
            body_checks.append(check)
        
        body_group.setLayout(body_layout)
        self.content_layout.addWidget(body_group)
        
        # SECOND ROW: Two columns for space and intensity
        second_row_layout = QHBoxLayout()
        second_row_layout.setSpacing(30)
        
        # Left column: Available Space
        space_group = QGroupBox("Available Space")
        space_group.setStyleSheet(body_group.styleSheet())
        space_layout = QVBoxLayout()
        
        space_combo = QComboBox()
        space_combo.addItems(["Small", "Medium", "Large"])
        space_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 12px;
                font-size: 16px;
            }
            QComboBox QAbstractItemView {
                background: rgba(255, 255, 255, 0.2);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                selection-background-color: rgba(59, 130, 246, 0.5);
            }
        """)
        
        # Load existing space selection
        if 'available_space' in self.user_data:
            space_combo.setCurrentText(self.user_data['available_space'])
        
        # Save when selection changes
        space_combo.currentTextChanged.connect(lambda text: self.update_user_data('available_space', text))
        
        space_layout.addWidget(space_combo)
        space_group.setLayout(space_layout)
        second_row_layout.addWidget(space_group)
        
        # Right column: Preferred Intensity
        intensity_group = QGroupBox("Preferred Intensity")
        intensity_group.setStyleSheet(body_group.styleSheet())
        intensity_layout = QVBoxLayout()
        intensity_layout.setSpacing(15)
        
        # Slider
        intensity_slider = QSlider(Qt.Horizontal)
        intensity_slider.setMinimum(1)
        intensity_slider.setMaximum(10)
        
        # Load existing intensity
        if 'intensity' in self.user_data:
            intensity_slider.setValue(self.user_data['intensity'])
        else:
            intensity_slider.setValue(5)  # Default middle
        
        intensity_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3b82f6;
                width: 20px;
                height: 20px;
                border-radius: 10px;
                margin: -6px 0;
            }
            QSlider::sub-page:horizontal {
                background: #3b82f6;
                border-radius: 4px;
            }
        """)
        
        # Save when slider changes
        intensity_slider.valueChanged.connect(lambda value: self.update_user_data('intensity', value))
        
        intensity_layout.addWidget(intensity_slider)
        
        # Labels for slider ends
        labels_layout = QHBoxLayout()
        relaxed_label = QLabel("Relaxed")
        extreme_label = QLabel("Extreme")
        
        for label in [relaxed_label, extreme_label]:
            label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                background: transparent;
            """)
        
        labels_layout.addWidget(relaxed_label)
        labels_layout.addStretch()
        labels_layout.addWidget(extreme_label)
        intensity_layout.addLayout(labels_layout)
        
        value_label = QLabel("5/10")
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            color: #3b82f6;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
            padding: 5px;
        """)
        intensity_layout.addWidget(value_label)

        # Connect slider to update value label
        def update_intensity_value(value):
            value_label.setText(f"{value}/10")
            self.update_user_data('intensity', value)

        intensity_slider.valueChanged.connect(update_intensity_value)
        
        # Update label with current value
        current_intensity = self.user_data.get('intensity', 5)
        value_label.setText(f"{current_intensity}/10")
        
        intensity_group.setLayout(intensity_layout)
        second_row_layout.addWidget(intensity_group)
        
        # Make both groups equal width
        second_row_layout.setStretchFactor(space_group, 1)
        second_row_layout.setStretchFactor(intensity_group, 1)
        
        self.content_layout.addLayout(second_row_layout)
        
        # Add some spacing and stretch
        self.content_layout.addSpacing(20)
        self.content_layout.addStretch()
    
    
    def create_accessibility_step(self):
        title = QLabel("Accessibility")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        subtitle = QLabel("UI & Interaction settings")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            background: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(subtitle)
        
        self.content_layout.addSpacing(40)
        
        # Center container for the group box
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        
        # Interaction group - centered and half width
        interaction_group = QGroupBox("Interaction")
        interaction_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-size: 18px;
                font-weight: bold;
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Set fixed width to make it half screen
        interaction_group.setMaximumWidth(400)
        
        interaction_layout = QVBoxLayout()
        interaction_layout.setSpacing(15)
        
        # Audio cues option with toggle switch
        audio_widget = QWidget()
        audio_layout = QHBoxLayout(audio_widget)
        audio_layout.setContentsMargins(15, 12, 15, 12)
        
        # Left side: Text content
        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(2)
        
        audio_title = QLabel("Audio Cues")
        audio_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
        text_layout.addWidget(audio_title)
        
        audio_desc = QLabel("Spoken instructions and beeps")
        audio_desc.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px; background: transparent;")
        text_layout.addWidget(audio_desc)
        
        audio_layout.addWidget(text_widget)
        audio_layout.addStretch()
        
        # Right side: Toggle switch
        toggle_switch = QCheckBox()
        toggle_switch.setFixedSize(50, 30)
        
        # Load existing audio setting
        if 'audio_cues' in self.user_data:
            toggle_switch.setChecked(self.user_data['audio_cues'])
        
        toggle_switch.setStyleSheet("""
            QCheckBox {
                background: rgba(255, 255, 255, 0.2);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 15px;
            }
            QCheckBox::indicator {
                width: 26px;
                height: 26px;
                border-radius: 13px;
                background: white;
            }
            QCheckBox::indicator:unchecked {
                margin: 2px 22px 2px 2px;
            }
            QCheckBox::indicator:checked {
                margin: 2px 2px 2px 22px;
            }
        """)
        
        # Custom toggle switch behavior
        def update_toggle_style(state):
            if state == Qt.Checked:
                toggle_switch.setStyleSheet("""
                    QCheckBox {
                        background: #3b82f6;
                        border: 2px solid #3b82f6;
                        border-radius: 15px;
                    }
                    QCheckBox::indicator {
                        width: 26px;
                        height: 26px;
                        border-radius: 13px;
                        background: white;
                    }
                    QCheckBox::indicator:unchecked {
                        margin: 2px 22px 2px 2px;
                    }
                    QCheckBox::indicator:checked {
                        margin: 2px 2px 2px 22px;
                    }
                """)
            else:
                toggle_switch.setStyleSheet("""
                    QCheckBox {
                        background: rgba(255, 255, 255, 0.2);
                        border: 2px solid rgba(255, 255, 255, 0.3);
                        border-radius: 15px;
                    }
                    QCheckBox::indicator {
                        width: 26px;
                        height: 26px;
                        border-radius: 13px;
                        background: white;
                    }
                    QCheckBox::indicator:unchecked {
                        margin: 2px 22px 2px 2px;
                    }
                    QCheckBox::indicator:checked {
                        margin: 2px 2px 2px 22px;
                    }
                """)
            self.toggle_audio_cues(state)
        
        toggle_switch.stateChanged.connect(update_toggle_style)
        audio_layout.addWidget(toggle_switch)
        
        # Make the entire widget clickable to toggle the switch
        audio_widget.setCursor(Qt.PointingHandCursor)
        audio_widget.mousePressEvent = lambda event: toggle_switch.setChecked(not toggle_switch.isChecked())
        
        interaction_layout.addWidget(audio_widget)
        
        # Add separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background: rgba(255, 255, 255, 0.2); margin: 10px 15px;")
        interaction_layout.addWidget(separator)
        
        # Additional Notes Text Box
        notes_widget = QWidget()
        notes_layout = QVBoxLayout(notes_widget)
        notes_layout.setContentsMargins(15, 0, 15, 12)
        notes_layout.setSpacing(8)
        
        notes_title = QLabel("Additional Notes")
        notes_title.setStyleSheet("color: white; font-size: 16px; font-weight: bold; background: transparent;")
        notes_layout.addWidget(notes_title)
        
        notes_desc = QLabel("Any special requirements or preferences")
        notes_desc.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 14px; background: transparent;")
        notes_layout.addWidget(notes_desc)
        
        # Text edit box
        notes_textedit = QTextEdit()
        notes_textedit.setMaximumHeight(100)
        notes_textedit.setPlaceholderText("Type any additional accessibility requirements, preferences, or notes here...")
        notes_textedit.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                selection-background-color: rgba(59, 130, 246, 0.5);
            }
            QTextEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)
        
        # Load existing notes
        if 'accessibility_notes' in self.user_data:
            notes_textedit.setText(self.user_data['accessibility_notes'])
        
        # Save notes when text changes
        notes_textedit.textChanged.connect(lambda: self.update_user_data('accessibility_notes', notes_textedit.toPlainText()))
        
        notes_layout.addWidget(notes_textedit)
        interaction_layout.addWidget(notes_widget)
        
        interaction_group.setLayout(interaction_layout)
        
        center_layout.addWidget(interaction_group)
        center_layout.addStretch()
        
        self.content_layout.addLayout(center_layout)
        self.content_layout.addStretch()
    
    def create_review_step(self):
        title = QLabel("All Set!")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 10px;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        subtitle = QLabel("Review and save your profile")
        subtitle.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8); 
            font-size: 16px;
            background: transparent;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(subtitle)
        
        self.content_layout.addSpacing(40)
        
        # Center container for both boxes
        center_layout = QVBoxLayout()
        center_layout.setSpacing(30)
        center_layout.setAlignment(Qt.AlignCenter)
        
        success_msg = QLabel("Profile configured successfully!\n\nClick 'Finish' to begin your workout.")
        success_msg.setStyleSheet("""
            QLabel {
                color: white; 
                font-size: 18px;
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        success_msg.setAlignment(Qt.AlignCenter)
        success_msg.setWordWrap(True)
        success_msg.setMaximumHeight(600)
        success_msg.setMaximumWidth(800)
        center_layout.addWidget(success_msg, alignment=Qt.AlignCenter)  # Add alignment here

        # Summary box - centered with custom title
        summary_group = QGroupBox()  # Remove default title
        summary_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;  # Add space for custom title
            }
        """)
        summary_group.setMaximumWidth(800)  # Half screen width
        summary_group.setMinimumWidth(400)
        
        summary_layout = QVBoxLayout()
        summary_layout.setSpacing(15)
        summary_layout.setAlignment(Qt.AlignCenter)
        
        # Custom centered title
        summary_title = QLabel("Profile Summary")
        summary_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            background: transparent;
            padding: 0px;
            margin: 0px;
        """)
        summary_title.setAlignment(Qt.AlignCenter)
        summary_layout.addWidget(summary_title)
        
        summary_layout.addSpacing(10)  # Space between title and content
        
        # Generate summary items from JSON data
        summary_items = []
        
        # Age range
        age = self.user_data.get('age_range', 'Not selected')
        summary_items.append(f"Age Range: {age}")
        
        # Fitness level
        fitness = self.user_data.get('fitness_level', 'Not selected')
        summary_items.append(f"Fitness Level: {fitness}")
        
        # Health conditions
        health_conditions = self.user_data.get('health_conditions', [])
        if health_conditions:
            summary_items.append(f"Health Conditions: {', '.join(health_conditions)}")
        else:
            summary_items.append("Health Conditions: None selected")
        
        # Body parts
        body_parts = self.user_data.get('body_parts', [])
        if body_parts:
            # Show first 2 and count of others if many
            if len(body_parts) > 2:
                summary_items.append(f"Body Focus: {', '.join(body_parts[:2])} +{len(body_parts)-2} more")
            else:
                summary_items.append(f"Body Focus: {', '.join(body_parts)}")
        else:
            summary_items.append("Body Focus: None selected")
        
        # Available space
        space = self.user_data.get('available_space', 'Not selected')
        summary_items.append(f"Available Space: {space}")
        
        # Intensity
        intensity = self.user_data.get('intensity', 'Not selected')
        summary_items.append(f"Preferred Intensity: {intensity}/10")
        
        # Audio cues
        audio = self.user_data.get('audio_cues', False)
        summary_items.append(f"Audio Cues: {'Enabled' if audio else 'Disabled'}")
        
        for item in summary_items:
            item_label = QLabel(item)
            item_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                background: transparent;
                padding: 2px;
            """)
            item_label.setAlignment(Qt.AlignCenter)
            summary_layout.addWidget(item_label)
        
        summary_group.setLayout(summary_layout)
        center_layout.addWidget(summary_group, alignment=Qt.AlignCenter)
        
        # Add the centered layout to main content
        self.content_layout.addLayout(center_layout)
        self.content_layout.addStretch()
    
    def next_step(self):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.clear_step_content()
            self.update_step()
        else:
            # Finish configuration - data is already saved in JSON
            print("Profile saved to:", self.config_file)
            print("User data:", self.user_data)
            
            if self.parent():
                self.parent().setCurrentIndex(2)  # Go back to home page
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.clear_step_content()
            self.update_step()
    
    def go_to_home(self):
        """Navigate to the home page"""
        main_app = self.parent()
        if main_app and main_app.count() > 0:
            main_app.setCurrentIndex(0)  # Home page should be at index 0

    def clear_step_content(self):
        # Remove all items (widgets and layouts) from content_layout
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                # Recursively clear nested layouts
                self.clear_layout(item.layout())
        
    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    self.clear_layout(item.layout())