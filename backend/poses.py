# poses.py
import cv2
import threading
import time
from posture import armsUp, squat, lunges, plank, touchToesFront, cobraStretch, treePose
from geminiFeedback import generate
from tts import speak_feedback

CHANGE_THRESHOLD = 8
FRAMES_REQUIRED = 2.1
STABILITY_WINDOW = 1.5
AUDIO_COOLDOWN = 2.0

EXERCISES_INFO = {
    "armsUp": "Arms Up:\nRaise both arms overhead until fully extended.\nKeep wrists above shoulders.",
    "squat": "Squat:\nLower your body by bending knees and hips.\nKeep your back straight and knees over toes.",
    # add all other exercises here
}

def run_exercise_loop(exercise_name, user_profile):
    """Generator function that yields (frame, feedback) tuples for PyQt to display."""
    exercise_map = {
        "Arms Up Stretch": armsUp,
        "Bodyweight Squat": squat,
        "Forward Lunge": lunges,
        "Plank": plank,
        "Toe Touch Stretch": touchToesFront,
        "Cobra Stretch": cobraStretch,
        "Tree Pose": treePose,
        "Wall Push-Up": plank
    }

    if exercise_name not in exercise_map:
        raise ValueError(f"Exercise '{exercise_name}' not found")

    exercise_func = exercise_map[exercise_name]

    latest_feedback = ""
    stable_feedback = ""
    last_exercise_data = None
    last_change_time = time.time()
    change_counter = 0
    last_feedback_time = 0
    last_audio_time = 0

    feedback_lock = threading.Lock()

    def feedback_worker(exerciseData):
        nonlocal latest_feedback
        new_feedback = generate(exerciseData, user_profile)
        with feedback_lock:
            latest_feedback = new_feedback

    def speak_feedback_thread(text):
        threading.Thread(target=speak_feedback, args=(text,), daemon=True).start()

    def has_significant_change(prev, curr):
        nonlocal change_counter
        if prev is None:
            return True
        big_change = any(
            isinstance(curr[k], (int, float)) and not isinstance(curr[k], bool) and prev.get(k) is not None and abs(prev[k] - curr[k]) > CHANGE_THRESHOLD
            for k in curr
        )
        bool_change = any(isinstance(curr[k], bool) and prev.get(k) is not None and prev[k] != curr[k] for k in curr)
        if big_change or bool_change:
            change_counter += 1
        else:
            change_counter = 0
        return change_counter >= FRAMES_REQUIRED

    def draw_wrapped_text(frame, text, x=30, y=120, dy=25, max_width=600, color=(0,255,0)):
        for line in text.splitlines():
            words = line.split(' ')
            current_line = ''
            for word in words:
                test_line = current_line + (' ' if current_line else '') + word
                (w, h), _ = cv2.getTextSize(test_line, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
                if w > max_width:
                    cv2.putText(frame, current_line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    y += dy
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                cv2.putText(frame, current_line, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                y += dy

    # Main loop: yield frames
    for frame, exerciseData in exercise_func():
        frame = cv2.flip(frame, 1)
        now = time.time()

        if has_significant_change(last_exercise_data, exerciseData):
            last_exercise_data = exerciseData.copy()
            if now - last_feedback_time > 2.0:
                last_feedback_time = now
                threading.Thread(target=feedback_worker, args=(exerciseData,), daemon=True).start()

        with feedback_lock:
            if latest_feedback != stable_feedback:
                stable_feedback = latest_feedback
                if user_profile.get("audio_cues", False):
                    if now - last_audio_time > AUDIO_COOLDOWN:
                        speak_feedback_thread(stable_feedback)
                        last_audio_time = now

        draw_wrapped_text(frame, stable_feedback)
        yield frame, stable_feedback
