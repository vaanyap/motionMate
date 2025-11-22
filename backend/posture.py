import cv2
import mediapipe as mp
import numpy as np

def calculateAngles(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    ba = a - b
    bc = c - b
    cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    return np.degrees(angle)

def armsUp():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)

            if results.pose_landmarks:
                keypoints = {}
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    keypoints[id] = (int(lm.x * w), int(lm.y * h))

                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                #poitns fore shoulder elbow and writs
                L_SH = keypoints[mpPose.PoseLandmark.LEFT_SHOULDER.value]
                L_EL = keypoints[mpPose.PoseLandmark.LEFT_ELBOW.value]
                L_WR = keypoints[mpPose.PoseLandmark.LEFT_WRIST.value]

                R_SH = keypoints[mpPose.PoseLandmark.RIGHT_SHOULDER.value]
                R_EL = keypoints[mpPose.PoseLandmark.RIGHT_ELBOW.value]
                R_WR = keypoints[mpPose.PoseLandmark.RIGHT_WRIST.value]

                #angles in generla
                L_ANGLE = calculateAngles(L_SH, L_EL, L_WR)
                R_ANGLE = calculateAngles(R_SH, R_EL, R_WR)

                #wristss
                left_up = L_WR[1] < L_SH[1]
                right_up = R_WR[1] < R_SH[1]


                armsUpStatus = left_up and right_up and L_ANGLE > 150 and R_ANGLE > 150

      
                exerciseData = {
                    "exercise": "armsUp",
                    "left_angle": L_ANGLE,
                    "right_angle": R_ANGLE,
                    "left_wrist_above_shoulder": left_up,
                    "right_wrist_above_shoulder": right_up,
                    "correct_form": armsUpStatus
                }

          
                cv2.putText(frame, f"L: {int(L_ANGLE)}°", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"R: {int(R_ANGLE)}°", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                yield frame, exerciseData
            else:
                # still yield the frame even if no landmarks
                yield frame, {
                    "exercise": "armsUp",
                    "left_angle": 0,
                    "right_angle": 0,
                    "left_wrist_above_shoulder": False,
                    "right_wrist_above_shoulder": False,
                    "correct_form": False
                }

    cap.release()


if __name__ == "__main__":
    for frame, data in armsUp():

        cv2.imshow("Arms Up Detection", frame)

       #q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
