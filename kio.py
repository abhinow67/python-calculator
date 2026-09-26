"""
Hand Gesture Recognition using MediaPipe and OpenCV
----------------------------------------------------
Detects hand landmarks in real-time from webcam feed
and classifies gestures:
  -  Fist
  -  Open Hand
  -  Thumbs Up
  - 👇 Thumbs Down
  - ✌️  Peace / Victory
  - ☝️  Pointing (Index Up)
  - 🤙 Call Me (Thumb + Pinky)

Requirements:
    pip install opencv-python mediapipe
"""

import cv2
import mediapipe as mp

# ── MediaPipe setup ─────────────────────────────────────────────────────────
mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils
mp_style = mp.solutions.drawing_styles

# Landmark indices (MediaPipe convention)
WRIST       = 0
THUMB_CMC   = 1;  THUMB_MCP   = 2;  THUMB_IP   = 3;  THUMB_TIP   = 4
INDEX_MCP   = 5;  INDEX_PIP   = 6;  INDEX_DIP  = 7;  INDEX_TIP   = 8
MIDDLE_MCP  = 9;  MIDDLE_PIP  = 10; MIDDLE_DIP = 11; MIDDLE_TIP  = 12
RING_MCP    = 13; RING_PIP    = 14; RING_DIP   = 15; RING_TIP    = 16
PINKY_MCP   = 17; PINKY_PIP   = 18; PINKY_DIP  = 19; PINKY_TIP   = 20


# ── Helper utilities ─────────────────────────────────────────────────────────
def landmark_list(hand_landmarks):
    """Return list of (x, y) tuples for all 21 landmarks (normalised 0-1)."""
    return [(lm.x, lm.y) for lm in hand_landmarks.landmark]


def finger_extended(lm, tip, pip, is_thumb=False, handedness="Right"):
    """
    Return True if the given finger is extended.
    For the thumb, a side-to-side comparison is used.
    For other fingers, tip must be above pip (smaller y = higher in frame).
    """
    if is_thumb:
        # Thumb extends left for right hand, right for left hand
        if handedness == "Right":
            return lm[tip][0] < lm[pip][0]
        else:
            return lm[tip][0] > lm[pip][0]
    else:
        return lm[tip][1] < lm[pip][1]


def get_finger_states(lm, handedness="Right"):
    """Return (thumb, index, middle, ring, pinky) booleans."""
    thumb  = finger_extended(lm, THUMB_TIP,  THUMB_IP,  is_thumb=True, handedness=handedness)
    index  = finger_extended(lm, INDEX_TIP,  INDEX_PIP)
    middle = finger_extended(lm, MIDDLE_TIP, MIDDLE_PIP)
    ring   = finger_extended(lm, RING_TIP,   RING_PIP)
    pinky  = finger_extended(lm, PINKY_TIP,  PINKY_PIP)
    return thumb, index, middle, ring, pinky


def classify_gesture(lm, handedness="Right"):
    """Map finger states to a gesture name + emoji."""
    t, i, m, r, p = get_finger_states(lm, handedness)

    # Thumb direction for thumbs-up / thumbs-down
    thumb_up   = lm[THUMB_TIP][1] < lm[THUMB_MCP][1]   # tip above knuckle
    thumb_down = lm[THUMB_TIP][1] > lm[WRIST][1]        # tip below wrist

    patterns = {
        # (thumb, index, middle, ring, pinky)
        (False, False, False, False, False): ("Fist",         "✊"),
        (True,  True,  True,  True,  True ): ("Open Hand",   "✋"),
        (False, True,  True,  False, False): ("Peace",       "✌️"),
        (False, True,  False, False, False): ("Pointing",    "☝️"),
        (True,  False, False, False, True ): ("Call Me",     "🤙"),
        (True,  True,  False, False, False): ("Gun / L",     "🤏"),
        (False, False, False, False, True ): ("Pinky Up",    "🤙"),
    }

    state = (t, i, m, r, p)

    # Special-case thumbs up / down (only thumb extended)
    if state == (True, False, False, False, False):
        if thumb_up:
            return "Thumbs Up", "👍"
        elif thumb_down:
            return "Thumbs Down", "👇"
        return "Thumbs Up", "👍"

    return patterns.get(state, ("Unknown", "❓"))


# ── Overlay drawing ──────────────────────────────────────────────────────────
FONT      = cv2.FONT_HERSHEY_DUPLEX
BOX_COLOR = (30, 30, 30)
TXT_COLOR = (255, 255, 255)
ACC_COLOR = (0, 220, 120)   # accent green


def draw_gesture_label(frame, gesture, emoji, hand_index=0):
    y_offset = 60 + hand_index * 90
    label = f"{gesture}"

    # Background pill
    (w, h), _ = cv2.getTextSize(label, FONT, 1.0, 2)
    cv2.rectangle(frame, (14, y_offset - 38), (26 + w, y_offset + 10),
                  BOX_COLOR, -1, cv2.LINE_AA)

    # Accent bar
    cv2.rectangle(frame, (14, y_offset - 38), (20, y_offset + 10),
                  ACC_COLOR, -1, cv2.LINE_AA)

    cv2.putText(frame, label, (28, y_offset),
                FONT, 1.0, ACC_COLOR, 2, cv2.LINE_AA)


def draw_fps(frame, fps):
    cv2.putText(frame, f"FPS: {fps:.0f}", (14, 30),
                FONT, 0.7, (180, 180, 180), 1, cv2.LINE_AA)


# ── Main loop ────────────────────────────────────────────────────────────────
def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌  Cannot open webcam. Check that a camera is connected.")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    import time
    prev_time = time.time()

    with mp_hands.Hands(
        model_complexity=1,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6,
    ) as hands:

        print("✋  Hand Gesture Recognition started. Press Q to quit.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)            # mirror view
            rgb   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            # FPS
            now = time.time()
            fps = 1.0 / (now - prev_time + 1e-9)
            prev_time = now
            draw_fps(frame, fps)

            if result.multi_hand_landmarks:
                for idx, (hand_lm, hand_info) in enumerate(
                    zip(result.multi_hand_landmarks,
                        result.multi_handedness)
                ):
                    handedness = hand_info.classification[0].label  # "Left" / "Right"

                    # Draw skeleton
                    mp_draw.draw_landmarks(
                        frame, hand_lm,
                        mp_hands.HAND_CONNECTIONS,
                        mp_style.get_default_hand_landmarks_style(),
                        mp_style.get_default_hand_connections_style(),
                    )

                    lm = landmark_list(hand_lm)
                    gesture, emoji = classify_gesture(lm, handedness)
                    draw_gesture_label(frame, f"{emoji} {gesture} ({handedness})", emoji, idx)

            cv2.imshow("Hand Gesture Recognition — press Q to quit", frame)

            if cv2.waitKey(1) & 0xFF in (ord("q"), ord("Q"), 27):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("👋  Goodbye!")


if __name__ == "__main__":
    main()