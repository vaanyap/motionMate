from posture import armsUp, squat, lunges, plank, touchToesFront, cobraStretch, treePose
from geminiFeedback import generate
import cv2
import threading
import sys
import json
import time
from tts import speak_feedback

latest_feedback = ""
displayed_feedback = ""  
last_exercise_data = None
feedback_lock = threading.Lock()  


with open("user_profile.json") as f:
    user_profile = json.load(f)

#audio
last_audio_time = 0
last_spoken_text = ""  
MIN_FEEDBACK_INTERVAL = 5.0
last_feedback_time = 0
AUDIO_COOLDOWN = 2.0

change_counter = 0
CHANGE_THRESHOLD = 8
FRAMES_REQUIRED = 2.1
STABILITY_WINDOW = 1.5 


EXERCISES_INFO = {
    "armsUp": "Arms Up:\nRaise both arms overhead until fully extended.\nKeep wrists above shoulders.",
    "squat": "Squat:\nLower your body by bending knees and hips.\nKeep your back straight and knees over toes.",
    
    
}

def feedback_worker(exerciseData):
    global latest_feedback
    new_feedback = generate(exerciseData, user_profile)
    with feedback_lock:
        latest_feedback = new_feedback

def speak_feedback_thread(text):
    threading.Thread(target=speak_feedback, args=(text,), daemon=True).start()

def has_significant_change(prev, curr):
    global change_counter
    if prev is None:
        return True

    big_change = any(
        isinstance(curr[k], (int, float)) \
and not isinstance(curr[k], bool) \
and prev.get(k) is not None \
and abs(float(prev[k]) - float(curr[k])) > CHANGE_THRESHOLD

        for k in curr
    )


    bool_change = any(
        isinstance(curr[k], bool) and prev.get(k) is not None and prev[k] != curr[k]
        for k in curr
    )

    if big_change or bool_change:
        change_counter += 1
    else:
        change_counter = 0

    return change_counter >= FRAMES_REQUIRED

def show_exercise_description(frame, text):
    y0, dy = 50, 30
    for i, line in enumerate(text.splitlines()):
        cv2.putText(frame, line, (50, y0 + i*dy), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)



if len(sys.argv) < 2:
    print("Usage: python main.py <exerciseName>")
    sys.exit(1)

exercise_name = sys.argv[1]
exercise_map = {
    "armsUp": armsUp,
    "squat": squat,
    "lunge": lunges,
    "plank": plank,
    "touchtoes": touchToesFront,
    "cobraStretch": cobraStretch,
    "treePose": treePose}





if exercise_name not in exercise_map:
    print(f"Exercise '{exercise_name}' not found. Available: {list(exercise_map.keys())}")
    sys.exit(1)

exercise_func = exercise_map[exercise_name]


last_spoken_text = ""  

stable_feedback = ""
latest_feedback_candidate = ""
last_change_time = time.time()


description = EXERCISES_INFO.get(exercise_name, "")
desc_start_time = time.time()
DESC_DURATION = 4 
def draw_wrapped_text(frame, text, x=30, y=120, dy=25, max_width=600, color=(0,255,0)):
    """
    Draws multi-line text on frame, wrapping long lines, using a single color.
    """
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

for frame, exerciseData in exercise_func():
    frame = cv2.flip(frame, 1)
    now = time.time()

    if has_significant_change(last_exercise_data, exerciseData):
        last_exercise_data = exerciseData.copy()
        if now - last_feedback_time > MIN_FEEDBACK_INTERVAL:
            last_feedback_time = now
            threading.Thread(target=feedback_worker, args=(exerciseData,), daemon=True).start()


    with feedback_lock:
        if latest_feedback != latest_feedback_candidate:
            latest_feedback_candidate = latest_feedback
            last_change_time = now  

   
    if now - last_change_time > STABILITY_WINDOW:
        if stable_feedback != latest_feedback_candidate:
            stable_feedback = latest_feedback_candidate

            if user_profile.get("accessibility", {}).get("audioCues", False):
                if now - last_audio_time > AUDIO_COOLDOWN:
                    speak_feedback_thread(stable_feedback)
                    last_audio_time = now



    color = (255, 200, 0)


    draw_wrapped_text(frame, stable_feedback, x=30, y=120, dy=25, max_width=600, color=color)



    cv2.imshow(f"{exercise_name} Exercise with Gemini Feedback", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
