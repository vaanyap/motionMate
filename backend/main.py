from posture import armsUp
from geminiFeedback import generate
import cv2
import threading

latest_feedback = ""  # shared variable to store the most recent feedback

def get_feedback_thread(exerciseData):
    global latest_feedback
    latest_feedback = generate(exerciseData)  # run Gemini in background

# main loop
for frame, exerciseData in armsUp():
    # launch feedback request every N frames or seconds if you want
    # for simplicity, launching a thread for each frame (can be optimized)
    threading.Thread(target=get_feedback_thread, args=(exerciseData,), daemon=True).start()

    # Display feedback (from last completed call)
    y0 = 120
    dy = 25
    for i, line in enumerate(latest_feedback.splitlines()):
        cv2.putText(frame, line, (30, y0 + i*dy), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                    (0,255,0) if exerciseData['correct_form'] else (0,0,255), 2)

    cv2.imshow("Arms Up Exercise with Gemini Feedback", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
