# 🦖 AI Dino Gesture Control (ML Edition)

A real-time Machine Learning & Computer Vision project that lets you play the classic Google Chrome Dinosaur game using custom hand gestures. Built with Python, OpenCV, Google MediaPipe, and Scikit-Learn.

Unlike basic state-machine controllers, this project features a full AI pipeline. You collect your own gesture data, train a Random Forest classifier to recognize your specific hands, and map those predictions to virtual keyboard inputs!

## ✨ Features & Pipeline

This project is split into three powerful stages:

1. **Data Collection:** Easily record 3D hand landmarks for different gestures via your webcam.
2. **AI Brain Training:** Train a custom Random Forest ML model on your recorded data to recognize gestures with high accuracy.
3. **Real-time Gameplay:** The AI processes live webcam feed to trigger game controls instantly.

### Default Gestures & Controls

- 👍 **Jump (Thumbs Up):** Jumps over cacti (Triggers `Spacebar`).
- 👎 **Duck (Thumbs Down):** Ducks under flying Pterodactyls (Holds `Down Arrow`).
- ✋ **Run (Flat Palm):** Runs normally (Releases all keys).
- ✌️ **Pause (Peace Sign):** Custom gesture label (Included for dataset gathering).

## 🛠️ Tech Stack

- **Python 3.11**
- **OpenCV (`opencv-python`):** For webcam video capture and image processing.
- **MediaPipe (`mediapipe==0.10.9`):** For 3D real-time hand tracking and landmark extraction.
- **Scikit-Learn (`scikit-learn`):** For the Random Forest machine learning algorithm.
- **Pandas (`pandas`):** For dataset management and data structuring.
- **PyAutoGUI (`pyautogui`):** To simulate keyboard presses.

## 🚀 Installation & Setup (Mac Apple Silicon / M-Series)

Modern macOS environments (M1/M2/M3) have strict security protocols for Python packages. Follow these exact steps in your terminal to set up a clean, working environment.

### 1. Install a Supported Python Version

Install Python 3.11 via Homebrew to avoid system conflicts:

```bash
brew install python@3.11
```

### 2. Create and Activate a Virtual Environment

Create a private "bubble" for this project using your newly installed Python 3.11:

```bash
python3.11 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

_(Note: You must run this activation command every time you open a new terminal to work on or play the game)._

### 3. Install Dependencies

Install the required libraries. **Crucial:** We pin MediaPipe to version `0.10.9` to ensure the `mp.solutions.hands` module functions correctly.

```bash
pip install opencv-python mediapipe==0.10.9 pyautogui pandas scikit-learn --no-cache-dir
```

## 🔒 Granting macOS Accessibility Permissions

Because this script simulates physical keyboard presses (`pyautogui`), macOS will block it by default for security reasons. Before playing:

1. Open **System Settings > Privacy & Security > Accessibility**.
2. Find your Terminal application (or VS Code).
3. Toggle the switch to **ON**. (You may need to enter your Mac password).

## 🎮 How to Train & Play

Ensure your virtual environment is active (`venv`), then follow this 3-step pipeline:

### Step 1: Collect Your Data

Run the data collector to teach the AI what your gestures look like.

```bash
python collect_data.py
```

_Press `0`, `1`, `2`, or `3` to record 500 samples of each gesture. Hold your hand in front of the camera until it finishes recording the current label._

### Step 2: Train the AI Brain

Once data is collected (saved as `gesture_data.csv`), train the machine learning model.

```bash
python train_model.py
```

_This script will output the accuracy of your model and save it as `gesture_model.pkl`._

### Step 3: Play the Game

Run the main game controller script.

```bash
python play_dino_ml.py
```

Open Google Chrome, navigate to `chrome://dino`, click on the page to make it active, and use your hands to play!

### Quitting

To stop any of the programs safely, click on the camera window and press the `q` key on your keyboard.
