import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Open Mac Webcam
cap = cv2.VideoCapture(0)

# Track what the dinosaur is currently doing to prevent spamming keys
current_action = "run"  

print("Camera warming up... Open Chrome and go to chrome://dino")

# A quick helper function to check if a finger is open or closed
def is_finger_open(landmarks, tip_id, pip_id):
    # Remember: lower Y value means higher up on the screen
    return landmarks[tip_id].y < landmarks[pip_id].y

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip horizontally for a natural selfie-view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture_text = "Searching for Hand..."
    new_action = "run" # Default state

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check the status of all four fingers (ignoring the thumb for simplicity)
            lm = hand_landmarks.landmark
            index_open = is_finger_open(lm, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.INDEX_FINGER_PIP)
            middle_open = is_finger_open(lm, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP)
            ring_open = is_finger_open(lm, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP)
            pinky_open = is_finger_open(lm, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP)

            # Count how many fingers are currently sticking up
            open_fingers_count = sum([index_open, middle_open, ring_open, pinky_open])

            # Logic to determine the gesture
            if open_fingers_count == 0:
                gesture_text = "FIST -> DUCKING"
                new_action = "duck"
            elif open_fingers_count == 1 and index_open:
                gesture_text = "1 FINGER -> JUMP!"
                new_action = "jump"
            else:
                gesture_text = "OPEN HAND -> RUNNING"
                new_action = "run"

    # Only trigger the keyboard if your action actually changes!
    if new_action != current_action:
        # 1. If we were ducking, release the down arrow so we can stand up
        if current_action == "duck":
            pyautogui.keyUp('down')
        
        # 2. Trigger the new action
        if new_action == "jump":
            pyautogui.press('space') # A single tap to jump
        elif new_action == "duck":
            pyautogui.keyDown('down') # Hold the key down to stay ducked
            
        current_action = new_action # Update our current state

    # Display the current gesture on the camera feed
    cv2.putText(frame, gesture_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
    cv2.imshow("Dino Gesture Control Pro", frame)

    # Press 'q' to safely quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Safety cleanup: Ensure keys aren't stuck down when you quit
if current_action == "duck":
    pyautogui.keyUp('down')
cap.release()
cv2.destroyAllWindows()