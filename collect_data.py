import cv2
import mediapipe as mp
import pandas as pd
import os

# Initialize MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

csv_file = 'gesture_data.csv'

# Set up column names (x0, y0, z0, x1, y1, z1...)
columns = ['label']
for i in range(21):
    columns.extend([f'x{i}', f'y{i}', f'z{i}'])

if not os.path.exists(csv_file):
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_file, index=False)

cap = cv2.VideoCapture(0)
print("\n--- Data Collection Started ---")
print("Press '0' for Run (Flat Palm)")
print("Press '1' for Jump (Thumbs Up)")
print("Press '2' for Duck (Thumbs Down)")
print("Press '3' for Pause (Peace Sign)")
print("Press 'q' to Quit\n")

recording_label = None
samples_collected = 0     
TARGET_SAMPLES = 500

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if recording_label is not None and samples_collected < TARGET_SAMPLES:
                row_data = [recording_label]
                for lm in hand_landmarks.landmark:
                    row_data.extend([lm.x, lm.y, lm.z])
                
                df = pd.DataFrame([row_data])
                df.to_csv(csv_file, mode='a', header=False, index=False)
                samples_collected += 1
                
                cv2.putText(frame, f"Recording '{recording_label}': {samples_collected}/{TARGET_SAMPLES}", 
                            (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
            elif samples_collected == TARGET_SAMPLES:
                print(f"Finished recording label: {recording_label}")
                recording_label = None
                samples_collected = 0

    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('0'): recording_label, samples_collected = "Run", 0
    elif key == ord('1'): recording_label, samples_collected = "Jump", 0
    elif key == ord('2'): recording_label, samples_collected = "Duck", 0
    elif key == ord('3'): recording_label, samples_collected = "Pause", 0
    elif key == ord('q'): break

    cv2.imshow("Data Collector", frame)

cap.release()
cv2.destroyAllWindows()