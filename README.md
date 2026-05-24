# 🦖 Dino Gesture Control Pro

A real-time Computer Vision project that lets you play the classic Google Chrome Dinosaur game using hand gestures. Built with Python, OpenCV, and Google MediaPipe.

This project maps physical hand movements via your webcam to virtual keyboard inputs, allowing you to jump and duck without ever touching your keyboard!

## ✨ Features & Controls

The script acts as a smart state machine, recognizing three specific hand states to control the dinosaur:

- ☝️ **Index Finger Up:** Jumps over cacti (Triggers `Spacebar`).
- ✊ **Closed Fist:** Ducks under flying Pterodactyls (Holds `Down Arrow`).
- ✋ **Open Hand:** Runs normally (Releases all keys).

## 🛠️ Tech Stack

- **Python 3.11**
- **OpenCV (`opencv-python`):** For webcam video capture and image processing.
- **MediaPipe (`mediapipe==0.10.9`):** For 3D real-time hand tracking and landmark extraction.
- **PyAutoGUI (`pyautogui`):** To simulate keyboard presses on macOS.

## 🚀 Installation & Setup (Mac Apple Silicon / M-Series)

Modern macOS environments (M1/M2/M3) have strict security protocols for Python packages and specific compatibility requirements for MediaPipe. Follow these exact steps in your terminal to set up a clean, working environment.

### 1. Install a Supported Python Version

MediaPipe's `solutions` API requires a Python version between 3.8 and 3.12. Install Python 3.11 via Homebrew to avoid system conflicts:

```bash
brew install python@3.11
```

### 2. Create and Activate a Virtual Environment

To prevent the `externally-managed-environment` error, create a private "bubble" for this project using your newly installed Python 3.11:

```bash
python3.11 -m venv venv
```

Activate the environment:

```bash
source venv/bin/activate
```

_(Note: You must run this activation command every time you open a new terminal to play the game)._

### 3. Install Dependencies

Install the required libraries. **Crucial:** We pin MediaPipe to version `0.10.9` to ensure the classic `mp.solutions.hands` module functions correctly.

```bash
pip install opencv-python mediapipe==0.10.9 pyautogui --no-cache-dir
```

## 🔒 Granting macOS Accessibility Permissions

Because this script simulates physical keyboard presses (pyautogui), macOS will block it by default for security reasons. Before running the script for the first time:

1. Open **System Settings > Privacy & Security > Accessibility**.
2. Find your Terminal application (or VS Code, depending on where you run the script).
3. Toggle the switch to **ON**. (You may need to enter your Mac password).

## 🎮 How to Play

1. Ensure your virtual environment is active (`venv`).
2. Run the Python script:
   ```bash
   python dino_control.py
   ```
3. A camera window titled "Dino Gesture Control Pro" will open. Hold up your hand to ensure the tracking skeleton appears and the text correctly reads your gestures.
4. Open Google Chrome and navigate to:
   ```text
   chrome://dino
   ```
5. Click anywhere on the webpage with your mouse to make Chrome the active window.
6. Raise your index finger to start the game!

### Quitting

To stop the program safely, click on the camera window and press the `q` key on your keyboard.
