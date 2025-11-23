# camera_feed.py
import sys
import os
import json
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import cv2
import requests

# Add backend to path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from poses import run_exercise_loop

def cv_to_pixmap(frame):
    if frame is None:
        return QPixmap()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb.shape
    bytes_per_line = ch * w
    qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
    return QPixmap.fromImage(qimg)

class CameraFeedPage(QWidget):
    def __init__(self, recommended_exercises=None, recommended_exercise=None, user_profile_file="user_profile.json"):
        super().__init__()

        # Handle both single and multiple exercises
        if recommended_exercises is None:
            if recommended_exercise:
                recommended_exercises = [recommended_exercise]
            else:
                recommended_exercises = []
        self.recommended_exercises = recommended_exercises
        self.current_index = 0
        self.user_profile_file = user_profile_file
        self.exercise_gen = None
        self.timer = None
        self.session_active = True

        # UI Elements
        self.video_label = QLabel()
        self.video_label.setScaledContents(True)
        self.video_label.setMinimumSize(640, 480)
        
        # Top bar with End Session button
        top_bar = QHBoxLayout()

        # Exercise label (start empty)
        self.exercise_label = QLabel("Exercise: N/A")
        self.exercise_label.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        top_bar.addWidget(self.exercise_label)

        top_bar.addStretch()  # Push the End button to the right

        self.end_button = QPushButton("End Session")
        self.end_button.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold; padding: 8px;")
        self.end_button.clicked.connect(self.end_session)
        top_bar.addWidget(self.end_button)

        # Next Exercise button
        self.next_button = QPushButton("Next Exercise")
        self.next_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        self.next_button.clicked.connect(self.next_exercise)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.video_label)
        layout.addWidget(self.next_button)
        self.setLayout(layout)

        # Load user profile
        try:
            with open(self.user_profile_file) as f:
                self.user_profile = json.load(f)
        except:
            self.user_profile = {"level": "beginner", "goal": "strength"}

        # CRITICAL: Initialize seen_exercises as empty list if it doesn't exist
        # This ensures it starts fresh each session
        self.user_profile['seen_exercises'] = []
        self.save_user_profile()
        
        print(f"Initial user profile: {self.user_profile}")

        # Start first exercise if available
        if self.recommended_exercises:
            self.start_exercise(self.recommended_exercises[self.current_index])
        else:
            # If no exercises provided, get one from API
            self.get_new_exercise()

    def save_user_profile(self):
        """Save the updated user profile to file"""
        try:
            with open(self.user_profile_file, 'w') as f:
                json.dump(self.user_profile, f, indent=2)
            print(f"Saved user profile: {self.user_profile}")
        except Exception as e:
            print(f"Error saving user profile: {e}")

    def get_new_exercise(self):
        """Get a new exercise recommendation from the API"""
        try:
            print(f"Getting new exercise. Seen exercises: {self.user_profile.get('seen_exercises', [])}")
            response = requests.post("http://127.0.0.1:5000/recommend_exercise", json=self.user_profile)
            data = response.json()
            exercise_name = data.get("exercise_name", "pushup")
            
            print(f"API recommended: {exercise_name}")
            
            # Add to our exercises list
            if not self.recommended_exercises:
                self.recommended_exercises = []
            self.recommended_exercises.append(exercise_name)
            self.current_index = len(self.recommended_exercises) - 1
            
            self.start_exercise(exercise_name)
            return exercise_name
            
        except Exception as e:
            print("Failed to get recommendation:", e)
            # Fallback - use exercises not in seen list
            all_exercises = ["pushup", "squat", "plank", "lunges", "crunches"]
            unseen_exercises = [ex for ex in all_exercises if ex not in self.user_profile.get('seen_exercises', [])]
            
            if unseen_exercises:
                exercise_name = unseen_exercises[0]
            else:
                exercise_name = "pushup"  # Fallback if all exercises have been seen
                
            print(f"Using fallback exercise: {exercise_name}")
                
            if not self.recommended_exercises:
                self.recommended_exercises = []
            self.recommended_exercises.append(exercise_name)
            self.current_index = len(self.recommended_exercises) - 1
            
            self.start_exercise(exercise_name)
            return exercise_name

    def start_exercise(self, exercise_name):
        # Clean up previous exercise
        if self.timer and self.timer.isActive():
            self.timer.stop()
        if self.exercise_gen:
            try:
                self.exercise_gen.close()
            except:
                pass

        print(f"Starting: {exercise_name}")
        self.exercise_label.setText(f"Exercise: {exercise_name}")
        
        # Add to seen exercises ONLY when actually starting the exercise
        if exercise_name not in self.user_profile['seen_exercises']:
            self.user_profile['seen_exercises'].append(exercise_name)
            self.save_user_profile()
            print(f"Added {exercise_name} to seen_exercises")
        
        self.exercise_gen = run_exercise_loop(exercise_name, self.user_profile)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        try:
            if self.exercise_gen and self.session_active:
                frame, feedback = next(self.exercise_gen)
                self.video_label.setPixmap(cv_to_pixmap(frame))
        except StopIteration:
            self.timer.stop()
            print("Exercise complete! Press 'Next Exercise' to continue.")

    def next_exercise(self):
        if not self.session_active:
            return
            
        self.current_index += 1
        if self.current_index < len(self.recommended_exercises):
            next_exercise = self.recommended_exercises[self.current_index]
            self.start_exercise(next_exercise)
        else:
            # Get a new exercise from API
            self.get_new_exercise()

    def end_session(self):
        self.session_active = False
        if self.timer and self.timer.isActive():
            self.timer.stop()
        if self.exercise_gen:
            try:
                self.exercise_gen.close()
            except:
                pass
        
        self.video_label.clear()
        self.video_label.setText("Session Ended")
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("font-size: 24px; color: white; background-color: black;")
        
        self.next_button.setEnabled(False)
        self.end_button.setEnabled(False)
        print("Session ended by user.")
        print(f"Final seen_exercises: {self.user_profile.get('seen_exercises', [])}")