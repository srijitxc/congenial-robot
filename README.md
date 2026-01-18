# YouTube Hand Gesture Controller

A Python application that allows you to control YouTube videos using hand gestures detected via your webcam. Uses MediaPipe for hand tracking and OpenCV for video processing.

## Features

- **Play/Pause**: Show an open palm (👋)
- **Fullscreen Toggle**: Make a fist (✊)
- **Skip Backward 10s**: Swipe right (←)
- **Skip Forward 10s**: Swipe left (→)
- **Volume Up**: Swipe up (↑)
- **Volume Down**: Swipe down (↓)
- Real-time visual feedback with gesture indicators
- Cooldown mechanism to prevent accidental triggers

## Requirements

- Python 3.7+
- Webcam
- YouTube video playing in an active browser window

### Dependencies

- opencv-python
- mediapipe
- pyautogui

## Installation

1. Clone or download the project files.
2. Install the required packages:

   ```bash
   pip install opencv-python mediapipe pyautogui
   ```

## Usage

1. Ensure your webcam is connected and accessible.
2. Open a YouTube video in your browser and make the browser window active.
3. Run the script:

   ```bash
   python hand.py
   ```

4. A camera window will open showing your hand tracking.
5. Perform the gestures in front of the camera to control the video.
6. Press 'q' in the camera window to quit.

## Controls

| Gesture | Action | YouTube Shortcut |
|---------|--------|------------------|
| 👋 Open Palm | Play/Pause | K |
| ✊ Fist | Fullscreen Toggle | F |
| ← Swipe Right | Skip Backward 10s | J |
| → Swipe Left | Skip Forward 10s | L |
| ↑ Swipe Up | Volume Up | ↑ |
| ↓ Swipe Down | Volume Down | ↓ |

## Notes

- The application sends keyboard shortcuts to the active window, so ensure your YouTube tab is focused.
- Gesture detection requires good lighting and clear hand visibility.
- Adjust camera position for optimal tracking.
- The cooldown period prevents rapid successive gestures.

## Troubleshooting

- If the camera doesn't open, check your webcam permissions and connections.
- Ensure all dependencies are installed correctly.
- For best results, use a well-lit environment with your hand clearly visible to the camera.

## License

This project is open-source. Feel free to modify and distribute.