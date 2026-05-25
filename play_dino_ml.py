import cv2
import mediapipe as mp
import pyautogui
import pickle
import pandas as pd

# 1. Load your custom AI brain
print("Waking up the AI...")
try:
    with open('gesture_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    print("Error: Could not find gesture_model.pkl. Did you run train_model.py?")
    exit()

# 2. Recreate the exact column names we used for training
columns = []
for i in range(21):
    columns.extend([f'x{i}', f'y{i}', f'z{i}'])

# 3. Setup MediaPipe and Camera
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

# 4. Game State Machine
current_action = "Run"
print("Ready! Open Chrome and go to chrome://dino")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    gesture_text = "Searching..."
    new_action = "Run"

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract coordinates just like we did in the data collector
            row_data = []
            for lm in hand_landmarks.landmark:
                row_data.extend([lm.x, lm.y, lm.z])
            
            # Package the data for the AI
            df = pd.DataFrame([row_data], columns=columns)
            
            # Ask the AI what gesture this is!
            predicted_label = model.predict(df)[0]
            gesture_text = f"AI sees: {predicted_label}"
            new_action = predicted_label

    # 5. Keyboard Logic
    if new_action != current_action:
        # If we were ducking, release the key to stand up
        if current_action == "Duck":
            pyautogui.keyUp('down')
            
        # Trigger the new action
        if new_action == "Jump":
            pyautogui.press('space')
        elif new_action == "Duck":
            pyautogui.keyDown('down')
            
        current_action = new_action

    # Visual Feedback
    cv2.putText(frame, gesture_text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
    cv2.imshow("Custom AI Dino Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Safety cleanup
if current_action == "Duck":
    pyautogui.keyUp('down')
cap.release()
cv2.destroyAllWindows()                 