import cv2
import mediapipe as mp
import serial
import time

# --- Serial port config ---
# Change 'COM13' to your Arduino's port (Windows: COM3/COM4, Linux: /dev/ttyUSB0)
SERIAL_PORT = 'COM13'
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

# Landmark indices for fingertip and pip joints
TIPS = [4, 8, 12, 16, 20]   # Thumb, Index, Middle, Ring, Pinky
PIPS = [3, 6, 10, 14, 18]   # Joint below each tip

def get_finger_states(landmarks):
    """
    Returns a list of 5 ints: 1 = folded (servo 180°), 0 = extended (servo 0°)
    """
    states = []

    # --- Thumb: compare x-axis (horizontal fold) ---
    thumb_tip = landmarks[4]
    thumb_ip  = landmarks[3]
    # If thumb tip is closer to palm centre (landmark 9) than IP joint → folded
    palm_centre = landmarks[9]
    tip_dist = abs(thumb_tip.x - palm_centre.x)
    ip_dist  = abs(thumb_ip.x  - palm_centre.x)
    states.append(1 if tip_dist < ip_dist else 0)

    # --- Fingers 2–5: compare y-axis (tip above/below PIP) ---
    for tip_id, pip_id in zip(TIPS[1:], PIPS[1:]):
        tip_y = landmarks[tip_id].y
        pip_y = landmarks[pip_id].y
        # In image coords, y increases downward; tip_y > pip_y means finger curled down
        states.append(1 if tip_y > pip_y else 0)

    return states

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6) as hands:

    last_state = None

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        finger_states = [0, 0, 0, 0, 0]

        if result.multi_hand_landmarks:
            for hand_lm in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)
                finger_states = get_finger_states(hand_lm.landmark)

        # Build command string, e.g. "10110\n"
        cmd = ''.join(map(str, finger_states)) + '\n'

        # Only send if state changed (avoids flooding serial)
        if cmd != last_state:
            print("Sending:", cmd)
            ser.write(cmd.encode())
            last_state = cmd

        # Display finger states on frame
        labels = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        for i, (label, state) in enumerate(zip(labels, finger_states)):
            color = (0, 0, 220) if state else (0, 200, 0)
            text  = f"{label}: {'FOLD' if state else 'OPEN'}"
            cv2.putText(frame, text, (10, 30 + i * 28),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        cv2.imshow('Bionic Hand Tracker', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
ser.close()