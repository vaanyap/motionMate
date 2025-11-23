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


                armsUpStatus = left_up and right_up and L_ANGLE > 157 and R_ANGLE > 157

      
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

def squat():
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

                # Left side
                L_HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value]
                L_KNEE = keypoints[mpPose.PoseLandmark.LEFT_KNEE.value]
                L_ANKLE = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value]
                L_SHOULDER = keypoints[mpPose.PoseLandmark.LEFT_SHOULDER.value]

                # Right side
                R_HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value]
                R_KNEE = keypoints[mpPose.PoseLandmark.RIGHT_KNEE.value]
                R_ANKLE = keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value]
                R_SHOULDER = keypoints[mpPose.PoseLandmark.RIGHT_SHOULDER.value]

                # Knee angles (Hip-Knee-Ankle)
                left_knee_angle = calculateAngles(L_HIP, L_KNEE, L_ANKLE)
                right_knee_angle = calculateAngles(R_HIP, R_KNEE, R_ANKLE)

                # Torso angles (Shoulder-Hip-Ankle)
                left_torso_angle = calculateAngles(L_SHOULDER, L_HIP, L_ANKLE)
                right_torso_angle = calculateAngles(R_SHOULDER, R_HIP, R_ANKLE)

                # Criteria for proper squat
                knees_bent_enough = (60 <= left_knee_angle <= 110) and (60 <= right_knee_angle <= 110)
                back_straight = (120 <= left_torso_angle <= 180) and (120 <= right_torso_angle <= 180)
                correct_form = knees_bent_enough and back_straight

                exerciseData = {
                    "exercise": "squat",
                    "left_knee_angle": left_knee_angle,
                    "right_knee_angle": right_knee_angle,
                    "left_torso_angle": left_torso_angle,
                    "right_torso_angle": right_torso_angle,
                    "knees_bent_enough": knees_bent_enough,
                    "back_straight": back_straight,
                    "correct_form": correct_form
                }

                # Display angles
                cv2.putText(frame, f"L Knee: {int(left_knee_angle)}°", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"R Knee: {int(right_knee_angle)}°", (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"L Torso: {int(left_torso_angle)}°", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
                cv2.putText(frame, f"R Torso: {int(right_torso_angle)}°", (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

                yield frame, exerciseData
            else:
                yield frame, {
                    "exercise": "squat",
                    "left_knee_angle": 0,
                    "right_knee_angle": 0,
                    "left_torso_angle": 0,
                    "right_torso_angle": 0,
                    "knees_bent_enough": False,
                    "back_straight": False,
                    "correct_form": False
                }

    cap.release()


def lunges():
    """Standard forward lunges."""
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
                keypoints = {
                    id: (int(lm.x * w), int(lm.y * h), lm.visibility)  # add visibility
                    for id, lm in enumerate(results.pose_landmarks.landmark)
                }

                L_HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value]
                L_KNEE = keypoints[mpPose.PoseLandmark.LEFT_KNEE.value]
                L_ANKLE = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value]

                R_HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value]
                R_KNEE = keypoints[mpPose.PoseLandmark.RIGHT_KNEE.value]
                R_ANKLE = keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value]

                # --- Determine front leg using visibility (proxy for depth) ---
                left_depth = L_KNEE[2]
                right_depth = R_KNEE[2]

                if left_depth > right_depth:  # higher visibility = closer
                    front_knee = L_KNEE
                    front_hip = L_HIP
                    front_ankle = L_ANKLE
                else:
                    front_knee = R_KNEE
                    front_hip = R_HIP
                    front_ankle = R_ANKLE

                front_knee_angle = calculateAngles(front_hip[:2], front_knee[:2], front_ankle[:2])

                # Simple check: knee not too far over toes
                knee_not_over_toes = front_knee[0] < front_ankle[0] + 40

                correct = (70 <= front_knee_angle <= 12) and knee_not_over_toes

                exerciseData = {
                    "exercise": "lunges",
                    "front_knee_angle": front_knee_angle,
                    "knee_not_over_toes": knee_not_over_toes,
                    "correct_form": correct
                }

                yield frame, exerciseData   



    cap.release()


def touchToesFront():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mpPose.Pose(min_detection_confidence=0.5,
                     min_tracking_confidence=0.5) as pose:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)

            exerciseData = {
                "exercise": "touchToesFront",
                "hip_angle": 0,
                "arm_distance": 0,
                "correct_form": False
            }

            if results.pose_landmarks:
                keypoints = {
                    id: (int(lm.x * w), int(lm.y * h), lm.visibility)
                    for id, lm in enumerate(results.pose_landmarks.landmark)
                }

                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                # ----------------------------
                # Required points for front view
                # ----------------------------
                required_points = [
                    mpPose.PoseLandmark.LEFT_SHOULDER,
                    mpPose.PoseLandmark.RIGHT_SHOULDER,
                    mpPose.PoseLandmark.LEFT_HIP,
                    mpPose.PoseLandmark.RIGHT_HIP,
                    mpPose.PoseLandmark.LEFT_WRIST,
                    mpPose.PoseLandmark.RIGHT_WRIST,
                    mpPose.PoseLandmark.LEFT_ANKLE,
                    mpPose.PoseLandmark.RIGHT_ANKLE
                ]
                all_visible = all(keypoints[p.value][2] > 0.5 for p in required_points)
                if not all_visible:
                    yield frame, exerciseData
                    continue

                # Pick one side for simplicity (left)
                SH = keypoints[mpPose.PoseLandmark.LEFT_SHOULDER.value][:2]
                HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value][:2]
                WR = keypoints[mpPose.PoseLandmark.LEFT_WRIST.value][:2]
                ANK = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value][:2]

                # ----------------------------
                # Angles / distances
                # ----------------------------
                hip_angle = calculateAngles(SH, HIP, ANK)  # torso vs legs
                arm_distance = WR[1] - ANK[1]  # wrist vertical distance to ankle

                # ----------------------------
                # Form check
                # ----------------------------
                correct_form = hip_angle < 90 and arm_distance <= 50  # torso bent forward & hands near toes

                exerciseData.update({
                    "hip_angle": hip_angle,
                    "arm_distance": arm_distance,
                    "correct_form": correct_form
                })

                cv2.putText(frame, f"Good Form: {correct_form}", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0) if correct_form else (0, 0, 255), 2)

            yield frame, exerciseData

    cap.release()


def plank():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mpPose.Pose(min_detection_confidence=0.5,
                     min_tracking_confidence=0.5) as pose:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w = frame.shape[:2]
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)

            # Default data
            exerciseData = {
                "exercise": "plank",
                "correct_form": False,
                "torso_angle": 0
            }

            if results.pose_landmarks:
                keypoints = {
                    id: (int(lm.x * w), int(lm.y * h), lm.visibility)
                    for id, lm in enumerate(results.pose_landmarks.landmark)
                }
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                # ----------------------------
                # Side view: pick the shoulder closer to camera
                # ----------------------------
                L_SH = keypoints[mpPose.PoseLandmark.LEFT_SHOULDER.value]
                R_SH = keypoints[mpPose.PoseLandmark.RIGHT_SHOULDER.value]
                use_left = L_SH[0] < R_SH[0]

                if use_left:
                    SH = L_SH[:2]
                    HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value][:2]
                    ANK = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value][:2]
                else:
                    SH = R_SH[:2]
                    HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value][:2]
                    ANK = keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value][:2]

                # ----------------------------
                # Only evaluate if shoulder, hip, ankle visible
                # ----------------------------
                vis_points = [keypoints[p.value][2] for p in [
                    mpPose.PoseLandmark.LEFT_SHOULDER,
                    mpPose.PoseLandmark.RIGHT_SHOULDER,
                    mpPose.PoseLandmark.LEFT_HIP,
                    mpPose.PoseLandmark.RIGHT_HIP,
                    mpPose.PoseLandmark.LEFT_ANKLE,
                    mpPose.PoseLandmark.RIGHT_ANKLE
                ]]
                if min(vis_points) < 0.5:
                    yield frame, exerciseData
                    continue

                # --------------------
                # Torso/hip alignment from side view
                # --------------------
                torso_angle = calculateAngles(SH, HIP, ANK)  # side-view alignment

                # Only mark bad form if extreme collapse
                correct_form = 150 <= torso_angle <= 210  # flexible range

                exerciseData["torso_angle"] = torso_angle
                exerciseData["correct_form"] = correct_form

                # Draw feedback
                cv2.putText(frame, f"Good Form: {correct_form}", (20, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (0, 255, 0) if correct_form else (0, 0, 255), 2)

            yield frame, exerciseData

    cap.release()




def cobraStretch():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)

            # Default exercise data
            exerciseData = {
                "exercise": "cobraStretch",
                "torso_angle": 0,
                "elbow_angle": 0,
                "back_lifted": False,
                "arms_correct": False,
                "correct_form": False
            }

            if results.pose_landmarks:
                keypoints = {
                    id: (int(lm.x * w), int(lm.y * h), lm.visibility)
                    for id, lm in enumerate(results.pose_landmarks.landmark)
                }
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                required_points = [
                    mpPose.PoseLandmark.LEFT_SHOULDER,
                    mpPose.PoseLandmark.RIGHT_SHOULDER,
                    mpPose.PoseLandmark.LEFT_ELBOW,
                    mpPose.PoseLandmark.RIGHT_ELBOW,
                    mpPose.PoseLandmark.LEFT_HIP,
                    mpPose.PoseLandmark.RIGHT_HIP
                ]

                if all(keypoints[p.value][2] > 0.5 for p in required_points):
                    # Pick side closer to camera
                    L_SH = keypoints[mpPose.PoseLandmark.LEFT_SHOULDER.value]
                    R_SH = keypoints[mpPose.PoseLandmark.RIGHT_SHOULDER.value]
                    L_HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value]
                    R_HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value]

                    use_left = L_SH[0] < R_SH[0]

                    SH = L_SH if use_left else R_SH
                    HIP = L_HIP if use_left else R_HIP

                    SH_xy = SH[:2]
                    HIP_xy = HIP[:2]

                    # Approximate points above and below shoulder for torso angle
                    torso_angle = calculateAngles(
                        (HIP_xy[0], HIP_xy[1] + 50), SH_xy, (SH_xy[0], SH_xy[1] - 50)
                    )

                    # Less strict thresholds
                    back_lifted = 130 <= torso_angle <= 220  # allow some flexibility
                    extreme_back = torso_angle < 100 or torso_angle > 250

                    correct_form = back_lifted and not extreme_back

                    exerciseData.update({
                        "torso_angle": torso_angle,
                        "back_lifted": back_lifted,
                        "correct_form": correct_form
                    })

                    # Draw feedback on frame
                    cv2.putText(
                        frame, f"Cobra Form: {correct_form}", (20, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        (0, 255, 0) if correct_form else (0, 0, 255), 2
                    )

            # Show the frame in a window
            cv2.imshow("Cobra Stretch", frame)

            # Yield the data for other uses (e.g., Gemini)
            yield frame, exerciseData

            # Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def treePose():
    mpPose = mp.solutions.pose
    mpDraw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)

    with mpPose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            h, w, _ = frame.shape
            rgbFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgbFrame)

            exerciseData = {
                "exercise": "treePose",
                "support_knee_angle": 0,
                "foot_height_offset": 0,
                "correct_form": False
            }

            if results.pose_landmarks:
                keypoints = {
                    id: (int(lm.x*w), int(lm.y*h), lm.visibility)
                    for id, lm in enumerate(results.pose_landmarks.landmark)
                }
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

                required_points = [
                    mpPose.PoseLandmark.LEFT_HIP,
                    mpPose.PoseLandmark.RIGHT_HIP,
                    mpPose.PoseLandmark.LEFT_KNEE,
                    mpPose.PoseLandmark.RIGHT_KNEE,
                    mpPose.PoseLandmark.LEFT_ANKLE,
                    mpPose.PoseLandmark.RIGHT_ANKLE
                ]

                if all(keypoints[p.value][2] > 0.5 for p in required_points):
                    # Choose side supporting
                    left_support = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value][1] > keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value][1]
                    if left_support:
                        HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value]
                        KNEE = keypoints[mpPose.PoseLandmark.LEFT_KNEE.value]
                        ANKLE = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value]
                        R_HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value]
                        R_KNEE = keypoints[mpPose.PoseLandmark.RIGHT_KNEE.value]
                        R_ANKLE = keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value]
                    else:
                        HIP = keypoints[mpPose.PoseLandmark.RIGHT_HIP.value]
                        KNEE = keypoints[mpPose.PoseLandmark.RIGHT_KNEE.value]
                        ANKLE = keypoints[mpPose.PoseLandmark.RIGHT_ANKLE.value]
                        R_HIP = keypoints[mpPose.PoseLandmark.LEFT_HIP.value]
                        R_KNEE = keypoints[mpPose.PoseLandmark.LEFT_KNEE.value]
                        R_ANKLE = keypoints[mpPose.PoseLandmark.LEFT_ANKLE.value]

                    # Supporting leg straightness
                    support_knee_angle = calculateAngles(HIP[:2], KNEE[:2], ANKLE[:2])

                    # Foot height roughly inner thigh/calf
                    foot_height_offset = R_ANKLE[1] - KNEE[1]  # positive if foot higher than knee

                    correct = (140 <= support_knee_angle <= 180) and (0 <= foot_height_offset <= 120)  # relaxed thresholds

                    exerciseData.update({
                        "support_knee_angle": support_knee_angle,
                        "foot_height_offset": foot_height_offset,
                        "correct_form": correct
                    })

                    cv2.putText(frame, f"Tree Pose: {correct}", (20, 90),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (0, 255, 0) if correct else (0, 0, 255), 2)

            cv2.imshow("Tree Pose", frame)
            yield frame, exerciseData

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    for frame, data in armsUp():

        cv2.imshow("Arms Up Detection", frame)

       #q to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
