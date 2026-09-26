"""
Hand Gesture Classifier — Pure Python (no external libraries)
=============================================================
Classifies hand gestures from 21 MediaPipe-style (x, y) landmarks.

Landmark layout (MediaPipe convention):
        8   12  16  20
        |   |   |   |
        7   11  15  19
        |   |   |   |
        6   10  14  18
        |   |   |   |
  4     5    9  13  17
  |     |
  3     |
  |   WRIST (0)
  2
  |
  1

Fingers: Thumb(1-4), Index(5-8), Middle(9-12), Ring(13-16), Pinky(17-20)
"""

# ---------------------------------------------------------------------------
# Landmark indices
# ---------------------------------------------------------------------------
WRIST       = 0
THUMB_CMC, THUMB_MCP, THUMB_IP, THUMB_TIP     = 1, 2, 3, 4
INDEX_MCP,  INDEX_PIP,  INDEX_DIP,  INDEX_TIP  = 5, 6, 7, 8
MIDDLE_MCP, MIDDLE_PIP, MIDDLE_DIP, MIDDLE_TIP = 9, 10, 11, 12
RING_MCP,   RING_PIP,   RING_DIP,   RING_TIP   = 13, 14, 15, 16
PINKY_MCP,  PINKY_PIP,  PINKY_DIP,  PINKY_TIP  = 17, 18, 19, 20


# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------
def finger_extended(lm, tip, pip, is_thumb=False, handedness="Right"):
    """
    Returns True if the finger is extended.
    - Thumb: side-to-side comparison (x-axis).
    - Other fingers: tip must be above pip (smaller y = higher in image).
    """
    if is_thumb:
        return lm[tip][0] < lm[pip][0] if handedness == "Right" \
               else lm[tip][0] > lm[pip][0]
    return lm[tip][1] < lm[pip][1]


def get_finger_states(lm, handedness="Right"):
    """Returns (thumb, index, middle, ring, pinky) as booleans."""
    return (
        finger_extended(lm, THUMB_TIP,  THUMB_IP,   is_thumb=True, handedness=handedness),
        finger_extended(lm, INDEX_TIP,  INDEX_PIP),
        finger_extended(lm, MIDDLE_TIP, MIDDLE_PIP),
        finger_extended(lm, RING_TIP,   RING_PIP),
        finger_extended(lm, PINKY_TIP,  PINKY_PIP),
    )


def classify_gesture(lm, handedness="Right"):
    """
    Given 21 landmarks and handedness, return (gesture_name, emoji).
    lm — list of (x, y) tuples, normalised to [0.0, 1.0].
    """
    t, i, m, r, p = get_finger_states(lm, handedness)

    # Thumb direction for thumbs-up / thumbs-down
    thumb_up   = lm[THUMB_TIP][1] < lm[THUMB_MCP][1]
    thumb_down = lm[THUMB_TIP][1] > lm[WRIST][1]

    # Thumb-only gestures
    if (t, i, m, r, p) == (True, False, False, False, False):
        if thumb_up:
            return "Thumbs Up",   "👍"
        elif thumb_down:
            return "Thumbs Down", "👇"
        return "Thumbs Up", "👍"

    gesture_map = {
        (False, False, False, False, False): ("Fist",       "✊"),
        (True,  True,  True,  True,  True ): ("Open Hand",  "✋"),
        (False, True,  True,  False, False): ("Peace",      "✌️"),
        (False, True,  False, False, False): ("Pointing",   "☝️"),
        (True,  False, False, False, True ): ("Call Me",    "🤙"),
        (True,  True,  False, False, False): ("L Shape",    "🤏"),
        (False, False, False, False, True ): ("Pinky Up",   "🤞"),
        (False, True,  True,  True,  True ): ("Four",       "🖐"),
        (True,  True,  True,  False, False): ("Three",      "🤟"),
        (False, True,  False, False, True ): ("Spider-Man", "🕷️"),
    }

    return gesture_map.get((t, i, m, r, p), ("Unknown", "❓"))


# ---------------------------------------------------------------------------
# Demo — run with hardcoded landmark samples
# ---------------------------------------------------------------------------

# Each sample: name, handedness, 21 (x, y) landmarks
# Landmarks are intentionally simplified to clearly represent each gesture.
# y-axis: 0.0 = top of frame, 1.0 = bottom.  x-axis: 0.0 = left, 1.0 = right.

SAMPLES = [
    {
        "label": "Fist (all fingers curled)",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.45, 0.82),  # 1  THUMB_CMC
            (0.40, 0.76),  # 2  THUMB_MCP
            (0.38, 0.71),  # 3  THUMB_IP
            (0.42, 0.67),  # 4  THUMB_TIP   — curled inward (x > IP for right hand)
            (0.52, 0.70),  # 5  INDEX_MCP
            (0.52, 0.62),  # 6  INDEX_PIP
            (0.52, 0.57),  # 7  INDEX_DIP
            (0.52, 0.60),  # 8  INDEX_TIP   — tip BELOW pip → curled
            (0.57, 0.69),  # 9  MIDDLE_MCP
            (0.57, 0.61),  # 10 MIDDLE_PIP
            (0.57, 0.56),  # 11 MIDDLE_DIP
            (0.57, 0.59),  # 12 MIDDLE_TIP  — curled
            (0.62, 0.70),  # 13 RING_MCP
            (0.62, 0.62),  # 14 RING_PIP
            (0.62, 0.57),  # 15 RING_DIP
            (0.62, 0.60),  # 16 RING_TIP    — curled
            (0.67, 0.72),  # 17 PINKY_MCP
            (0.67, 0.65),  # 18 PINKY_PIP
            (0.67, 0.61),  # 19 PINKY_DIP
            (0.67, 0.63),  # 20 PINKY_TIP   — curled
        ],
    },
    {
        "label": "Open Hand (all fingers extended)",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.43, 0.82),  # 1  THUMB_CMC
            (0.37, 0.75),  # 2  THUMB_MCP
            (0.32, 0.69),  # 3  THUMB_IP
            (0.26, 0.64),  # 4  THUMB_TIP   — extended (x < IP for right hand)
            (0.50, 0.68),  # 5  INDEX_MCP
            (0.50, 0.56),  # 6  INDEX_PIP
            (0.50, 0.46),  # 7  INDEX_DIP
            (0.50, 0.37),  # 8  INDEX_TIP   — extended
            (0.56, 0.67),  # 9  MIDDLE_MCP
            (0.56, 0.54),  # 10 MIDDLE_PIP
            (0.56, 0.43),  # 11 MIDDLE_DIP
            (0.56, 0.34),  # 12 MIDDLE_TIP  — extended
            (0.62, 0.68),  # 13 RING_MCP
            (0.62, 0.56),  # 14 RING_PIP
            (0.62, 0.46),  # 15 RING_DIP
            (0.62, 0.37),  # 16 RING_TIP    — extended
            (0.68, 0.71),  # 17 PINKY_MCP
            (0.68, 0.61),  # 18 PINKY_PIP
            (0.68, 0.53),  # 19 PINKY_DIP
            (0.68, 0.46),  # 20 PINKY_TIP   — extended
        ],
    },
    {
        "label": "Thumbs Up",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.45, 0.82),  # 1  THUMB_CMC
            (0.40, 0.74),  # 2  THUMB_MCP
            (0.35, 0.66),  # 3  THUMB_IP
            (0.30, 0.57),  # 4  THUMB_TIP   — tip ABOVE mcp (y < mcp.y) & x < IP
            (0.52, 0.70),  # 5  INDEX_MCP
            (0.52, 0.63),  # 6  INDEX_PIP
            (0.52, 0.58),  # 7  INDEX_DIP
            (0.52, 0.61),  # 8  INDEX_TIP   — curled
            (0.57, 0.69),  # 9  MIDDLE_MCP
            (0.57, 0.62),  # 10 MIDDLE_PIP
            (0.57, 0.57),  # 11 MIDDLE_DIP
            (0.57, 0.60),  # 12 MIDDLE_TIP  — curled
            (0.62, 0.70),  # 13 RING_MCP
            (0.62, 0.63),  # 14 RING_PIP
            (0.62, 0.58),  # 15 RING_DIP
            (0.62, 0.61),  # 16 RING_TIP    — curled
            (0.67, 0.72),  # 17 PINKY_MCP
            (0.67, 0.66),  # 18 PINKY_PIP
            (0.67, 0.62),  # 19 PINKY_DIP
            (0.67, 0.64),  # 20 PINKY_TIP   — curled
        ],
    },
    {
        "label": "Peace / Victory sign",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.43, 0.82),  # 1  THUMB_CMC
            (0.38, 0.76),  # 2  THUMB_MCP
            (0.36, 0.71),  # 3  THUMB_IP
            (0.40, 0.67),  # 4  THUMB_TIP   — curled
            (0.50, 0.68),  # 5  INDEX_MCP
            (0.50, 0.56),  # 6  INDEX_PIP
            (0.50, 0.46),  # 7  INDEX_DIP
            (0.50, 0.37),  # 8  INDEX_TIP   — extended ✓
            (0.56, 0.67),  # 9  MIDDLE_MCP
            (0.56, 0.54),  # 10 MIDDLE_PIP
            (0.56, 0.43),  # 11 MIDDLE_DIP
            (0.56, 0.34),  # 12 MIDDLE_TIP  — extended ✓
            (0.62, 0.68),  # 13 RING_MCP
            (0.62, 0.62),  # 14 RING_PIP
            (0.62, 0.57),  # 15 RING_DIP
            (0.62, 0.60),  # 16 RING_TIP    — curled
            (0.68, 0.71),  # 17 PINKY_MCP
            (0.68, 0.66),  # 18 PINKY_PIP
            (0.68, 0.62),  # 19 PINKY_DIP
            (0.68, 0.64),  # 20 PINKY_TIP   — curled
        ],
    },
    {
        "label": "Pointing (index only)",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.43, 0.82),  # 1  THUMB_CMC
            (0.38, 0.76),  # 2  THUMB_MCP
            (0.36, 0.71),  # 3  THUMB_IP
            (0.40, 0.67),  # 4  THUMB_TIP   — curled
            (0.50, 0.68),  # 5  INDEX_MCP
            (0.50, 0.56),  # 6  INDEX_PIP
            (0.50, 0.46),  # 7  INDEX_DIP
            (0.50, 0.37),  # 8  INDEX_TIP   — extended ✓
            (0.57, 0.69),  # 9  MIDDLE_MCP
            (0.57, 0.62),  # 10 MIDDLE_PIP
            (0.57, 0.57),  # 11 MIDDLE_DIP
            (0.57, 0.60),  # 12 MIDDLE_TIP  — curled
            (0.62, 0.70),  # 13 RING_MCP
            (0.62, 0.63),  # 14 RING_PIP
            (0.62, 0.58),  # 15 RING_DIP
            (0.62, 0.61),  # 16 RING_TIP    — curled
            (0.67, 0.72),  # 17 PINKY_MCP
            (0.67, 0.66),  # 18 PINKY_PIP
            (0.67, 0.62),  # 19 PINKY_DIP
            (0.67, 0.64),  # 20 PINKY_TIP   — curled
        ],
    },
    {
        "label": "Call Me (thumb + pinky)",
        "handedness": "Right",
        "landmarks": [
            (0.50, 0.90),  # 0  WRIST
            (0.43, 0.82),  # 1  THUMB_CMC
            (0.37, 0.75),  # 2  THUMB_MCP
            (0.31, 0.68),  # 3  THUMB_IP
            (0.25, 0.62),  # 4  THUMB_TIP   — extended ✓
            (0.52, 0.70),  # 5  INDEX_MCP
            (0.52, 0.63),  # 6  INDEX_PIP
            (0.52, 0.58),  # 7  INDEX_DIP
            (0.52, 0.61),  # 8  INDEX_TIP   — curled
            (0.57, 0.69),  # 9  MIDDLE_MCP
            (0.57, 0.62),  # 10 MIDDLE_PIP
            (0.57, 0.57),  # 11 MIDDLE_DIP
            (0.57, 0.60),  # 12 MIDDLE_TIP  — curled
            (0.62, 0.70),  # 13 RING_MCP
            (0.62, 0.63),  # 14 RING_PIP
            (0.62, 0.58),  # 15 RING_DIP
            (0.62, 0.61),  # 16 RING_TIP    — curled
            (0.67, 0.72),  # 17 PINKY_MCP
            (0.67, 0.62),  # 18 PINKY_PIP
            (0.67, 0.52),  # 19 PINKY_DIP
            (0.67, 0.43),  # 20 PINKY_TIP   — extended ✓
        ],
    },
]


def run_demo():
    print("=" * 58)
    print("   Hand Gesture Classifier — Pure Python Demo")
    print("=" * 58)
    print(f"{'Input Label':<35} {'Detected Gesture':<18} {'Emoji'}")
    print("-" * 58)

    all_pass = True
    for sample in SAMPLES:
        lm        = sample["landmarks"]
        handed    = sample["handedness"]
        gesture, emoji = classify_gesture(lm, handed)
        match = "✓" if any(w in sample["label"] for w in gesture.split()) else "?"
        if match == "?":
            all_pass = False
        print(f"{sample['label']:<35} {gesture:<18} {emoji}  {match}")

    print("-" * 58)
    print(f"All tests passed: {'YES ✓' if all_pass else 'CHECK ABOVE'}")
    print()
    print("To use with your own landmarks, call:")
    print("  classify_gesture(landmarks, handedness='Right')")
    print("  landmarks = list of 21 (x, y) tuples, values in [0.0, 1.0]")


if __name__ == "__main__":
    run_demo()