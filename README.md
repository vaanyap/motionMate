**MotionMate+**

AI-powered yoga posture analysis and personalized exercise feedback

Overview

MotionMate+ is an AI-powered application that evaluates yoga poses in real time using computer vision and provides personalized feedback to help users improve their form.

The system captures body landmarks using MediaPipe and analyzes joint angles to determine whether a pose is performed correctly. Based on this analysis, the application generates feedback and recommended exercises using an AI API.

The goal of MotionMate+ is to make posture correction and guided exercise more accessible by providing instant feedback without requiring a human trainer.

Features

Real-time pose detection using MediaPipe

Joint angle analysis to evaluate yoga posture accuracy

AI-generated feedback and exercise recommendations

Flask-based backend for processing pose data

Multithreaded processing to improve responsiveness and reduce latency

Tech Stack

Languages

Python

Frameworks & Libraries

Flask

OpenCV

MediaPipe

AI

Google Gemini API

How It Works

The application captures live webcam footage.

MediaPipe extracts body landmarks from each frame.

The system calculates joint angles to determine pose accuracy.

Pose data is sent to the backend.

The Gemini API generates personalized feedback and exercise recommendations.

The feedback is displayed to the user in real time.
