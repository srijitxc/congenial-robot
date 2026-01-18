
import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque
import math

class HandGestureYouTubeController:
    def __init__(self):
        # MediaPipe hand tracking
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Gesture detection
        self.hand_positions = deque(maxlen=10)
        self.last_gesture_time = 0
        self.gesture_cooldown = 1.0  # seconds
        self.last_gesture = None
        
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def detect_hand_state(self, hand_landmarks):
        """Detect if hand is open (palm) or closed (fist)"""
        # Get fingertip and base landmarks
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]
        ring_tip = hand_landmarks.landmark[16]
        pinky_tip = hand_landmarks.landmark[20]
        
        # Get palm center (landmark 0)
        palm = hand_landmarks.landmark[0]
        
        # Calculate distances from palm to fingertips
        thumb_dist = self.calculate_distance(thumb_tip, palm)
        index_dist = self.calculate_distance(index_tip, palm)
        middle_dist = self.calculate_distance(middle_tip, palm)
        ring_dist = self.calculate_distance(ring_tip, palm)
        pinky_dist = self.calculate_distance(pinky_tip, palm)
        
        avg_distance = (thumb_dist + index_dist + middle_dist + ring_dist + pinky_dist) / 5
        
        # Open hand (palm) has larger average distance
        if avg_distance > 0.25:
            return 'palm'
        # Closed hand (fist) has smaller average distance
        elif avg_distance < 0.15:
            return 'fist'
        return None
    
    def detect_swipe(self, current_pos):
        """Detect swipe gestures in all directions"""
        if len(self.hand_positions) < 5:
            self.hand_positions.append(current_pos)
            return None
        
        self.hand_positions.append(current_pos)
        
        # Calculate movement
        start_pos = self.hand_positions[0]
        end_pos = self.hand_positions[-1]
        movement_x = end_pos[0] - start_pos[0]
        movement_y = end_pos[1] - start_pos[1]
        
        # Check if enough time has passed since last gesture
        current_time = time.time()
        if current_time - self.last_gesture_time < self.gesture_cooldown:
            return None
        
        # Determine primary direction (horizontal or vertical)
        if abs(movement_x) > abs(movement_y):
            # Horizontal swipe
            if abs(movement_x) > 0.15:
                self.last_gesture_time = current_time
                self.hand_positions.clear()
                
                if movement_x > 0:
                    return 'right'  # Swipe right
                else:
                    return 'left'   # Swipe left
        else:
            # Vertical swipe
            if abs(movement_y) > 0.15:
                self.last_gesture_time = current_time
                self.hand_positions.clear()
                
                if movement_y < 0:
                    return 'up'     # Swipe up
                else:
                    return 'down'   # Swipe down
        
        return None
    
    def execute_youtube_command(self, gesture):
        """Execute YouTube keyboard shortcuts based on gesture"""
        commands = {
            'left': ('←', 'j', " Skip Backward 10s"),
            'right': ('→', 'l', " Skip Forward 10s"),
            'up': ('↑', 'up', " Volume Up"),
            'down': ('↓', 'down', " Volume Down"),
            'palm': ('👋', 'k', "⏯ Play/Pause"),
            'fist': ('✊', 'f', "⛶ Fullscreen Toggle")
        }
        
        if gesture in commands:
            symbol, key, description = commands[gesture]
            print(f"{symbol} {description}")
            
            # Send keyboard command to active window
            if key in ['up', 'down']:
                pyautogui.press(key)
            else:
                pyautogui.press(key)
            
            return description
        
        return None
    
    def draw_ui(self, frame, gesture_text=None):
        """Draw UI elements on frame"""
        height, width = frame.shape[:2]
        
        # Draw title bar
        cv2.rectangle(frame, (0, 0), (width, 100), (40, 40, 40), -1)
        cv2.putText(frame, "YouTube Hand Gesture Controller", 
                    (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, "Control ANY YouTube video! | Press 'q' to quit", 
                    (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        
        # Draw gesture guide
        guide_y = 110
        guides = [
            "👋 PALM → Play/Pause",
            "✊ FIST → Fullscreen",
            "← Swipe Right → Skip Back 10s",
            "Swipe Left → Skip Forward 10s",
            "↑ Swipe Up → Volume Up",
            "↓ Swipe Down → Volume Down"
        ]
        
        for i, guide in enumerate(guides):
            cv2.putText(frame, guide, (20, guide_y + i * 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 255, 150), 1)
        
        # Draw gesture indicator (large center display)
        if gesture_text:
            text_size = cv2.getTextSize(gesture_text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            x = (width - text_size[0]) // 2
            y = height // 2
            
            # Draw semi-transparent background
            overlay = frame.copy()
            cv2.rectangle(overlay, (x - 30, y - 60), (x + text_size[0] + 30, y + 20), 
                         (147, 51, 234), -1)
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
            
            cv2.putText(frame, gesture_text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
                       1.5, (255, 255, 255), 3)
        
        return frame
    
    def run(self):
        """Main loop"""
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open camera")
            return
        
        print("=" * 60)
        print("YouTube Hand Gesture Controller Started!")
        print("=" * 60)
        print("Make sure your YouTube video is playing in your browser")
        print("and that the browser window is active when using gestures.")
        print()
        print("Gestures:")
        print("  👋 Show PALM → Play/Pause")
        print("  ✊ Make FIST → Fullscreen Toggle")
        print("  ← Swipe RIGHT → Skip Backward 10 seconds")
        print("  Swipe LEFT → Skip Forward 10 seconds")
        print("  ↑ Swipe UP → Volume Up")
        print("  ↓ Swipe DOWN → Volume Down")
        print()
        print("Press 'q' in the camera window to quit")
        print("=" * 60)
        
        gesture_display = None
        gesture_display_time = 0
        hand_state_last = None
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            height, width = frame.shape[:2]
            
            # Convert to RGB for MediaPipe
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            gesture = None
            
            # Process hand landmarks
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw hand landmarks
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                        self.mp_draw.DrawingSpec(color=(255, 0, 255), thickness=2))
                    
                    # Get index finger tip position for swipe detection
                    index_tip = hand_landmarks.landmark[8]
                    current_pos = (index_tip.x, index_tip.y)
                    
                    # Detect swipe gesture
                    swipe = self.detect_swipe(current_pos)
                    if swipe:
                        gesture = swipe
                    
                    # Detect hand state (palm/fist) - only if no swipe detected
                    if not gesture:
                        hand_state = self.detect_hand_state(hand_landmarks)
                        current_time = time.time()
                        
                        # Only trigger on state change and after cooldown
                        if (hand_state and hand_state != hand_state_last and 
                            current_time - self.last_gesture_time > self.gesture_cooldown):
                            gesture = hand_state
                            hand_state_last = hand_state
                            self.last_gesture_time = current_time
            else:
                # Reset hand state when no hand detected
                hand_state_last = None
            
            # Execute command if gesture detected
            if gesture:
                gesture_text = self.execute_youtube_command(gesture)
                if gesture_text:
                    gesture_display = gesture_text
                    gesture_display_time = time.time()
            
            # Clear gesture display after 1.5 seconds
            if gesture_display and time.time() - gesture_display_time > 1.5:
                gesture_display = None
            
            # Draw UI
            frame = self.draw_ui(frame, gesture_display)
            
            # Display frame
            cv2.imshow('YouTube Hand Gesture Controller', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        self.hands.close()

if __name__ == "__main__":
    controller = HandGestureYouTubeController()
    controller.run()