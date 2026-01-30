import cv2
import mediapipe as mp
import time

from ui.light_controller import control_light
from ui.shutter_controller import control_shutter
from utils import clamp

# ================= MediaPipe =================
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= STATES =================
USER_SELECT = "user_select"
ROOM_SELECT = "room_select"
CONTROL_SELECT = "control_select"
LIGHT_CONTROL = "light_control"
SHUTTER_CONTROL = "shutter_control"

COOLDOWN = 1.2
last_action_time = 0

# ================= Finger-Erkennung =================
def fingers_up(hand):
    fingers = []
    # Daumen
    fingers.append(1 if hand.landmark[4].x < hand.landmark[3].x else 0)
    # Andere Finger
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0)
    return fingers


# ================= Handshape-Erkennung =================
def detect_handshape(f, hand=None):
    """Erkennt alle Gesten inklusive Daumen runter"""
    if f == [0,0,0,0,0]:
        return "fist"
    if f == [1,1,1,1,1]:
        return "open"
    if f == [0,1,0,0,0]:
        return "index"
    if f == [0,1,1,0,0]:
        return "index_middle"
        if f == [1,0,0,0,0]:  # Daumen
            if hand and hand.landmark[4].y > hand.landmark[2].y:  # <-- NEU: Daumen runter
                return "thumb_down"
            else:
                return "thumb_up"
    if f == [1,1,0,0,0]:
        return "thumb_index"
    if f == [0,0,1,0,0]:
        return "middle"  # Mittelfinger → zurück von Steuerung zu Raumwahl
    if f == [0,0,0,0,1]:
        return "pinky"   # kleiner Finger
    if f == [1,0,1,0,0]:
        return "thumb_middle"  # Daumen + Mittelfinger → zurück von Raumwahl zu Userwahl
    return "other"

# ================= Overlay =================
def draw_help(screen, font, state):
    x, y = 850, 100
    if state == USER_SELECT:
        lines = [
            "USER WAHL:",
            "☝ Zeigefinger → User 1",
            "✌ Zeigefinger+Mittel → User 2"
        ]
    elif state == ROOM_SELECT:
        lines = [
            "RAUM WAHL:",
            "☝ Zeigefinger → Raum 1",
            "✌ Zeigefinger+Mittel → Raum 2",
            "🖕 Mittelfinger → Zurück zu Userwahl"
        ]
    elif state == CONTROL_SELECT:
        lines = [
            "STEUERUNG:",
            "☝ Zeigefinger → Lichtsteuerung",
            "✌ Zeigefinger+Mittel → Rollosteuerung",
            "🖕 Mittelfinger → Zurück zu Raumwahl"
        ]
    elif state == LIGHT_CONTROL:
        lines = [
            "LICHT:",
            "👍 Daumen hoch → Heller",
            "👎 Daumen runter → Dunkler",
            "✊ Faust → Aus",
            "🤙 Kleiner Finger → An",
            "🖕 Mittelfinger → Zurück"
        ]
    elif state == SHUTTER_CONTROL:
        lines = [
            "ROLLO:",
            "👍 Daumen hoch → Hoch",
            "👎 Daumen runter → Runter",
            "✊ Faust → Auf",
            "🤙 Kleiner Finger → Zu",
            "🖕 Mittelfinger → Zurück"
        ]
    else:
        lines = ["Unbekannter State"]

    for line in lines:
        txt = font.render(line, True, (255, 255, 255))
        screen.blit(txt, (x, y))
        y += 30

# ================= Hauptfunktion =================
cap = cv2.VideoCapture(0)

def get_gesture_action(state, current_user, selected_room):
    global last_action_time

    ret, frame = cap.read()
    if not ret:
        return state, current_user, selected_room, None

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    now = time.time()

    if not result.multi_hand_landmarks or now - last_action_time < COOLDOWN:
        return state, current_user, selected_room, None

    hand = result.multi_hand_landmarks[0]
    handshape = detect_handshape(fingers_up(hand), hand)  # <-- NEU: hand übergeben für Daumen runter

    # ------------------ STATE MACHINE ------------------
    if state == USER_SELECT:
        if handshape == "index":
            current_user = "User 1"
            state = ROOM_SELECT
        elif handshape == "index_middle":
            current_user = "User 2"
            state = ROOM_SELECT

    elif state == ROOM_SELECT:
        if handshape == "index":
            selected_room = "Raum 1"
            state = CONTROL_SELECT
        elif handshape == "index_middle":
            selected_room = "Raum 2"
            state = CONTROL_SELECT
        elif handshape == "middle" or handshape == "thumb_middle":  # <-- NEU: beide zurück zur Userwahl
            state = USER_SELECT
            current_user = None
            selected_room = None

    elif state == CONTROL_SELECT:
        if handshape == "index":
            state = LIGHT_CONTROL
        elif handshape == "index_middle":
            state = SHUTTER_CONTROL
        elif handshape == "middle":  # zurück
            state = ROOM_SELECT
            selected_room = None

    elif state == LIGHT_CONTROL:
        if handshape == "thumb_up":
            control_light(selected_room, "up", current_user)
        elif handshape == "thumb_down":
            control_light(selected_room, "down", current_user)
        elif handshape == "fist":
            control_light(selected_room, "off", current_user)
        elif handshape == "pinky":
            control_light(selected_room, "on", current_user)
        elif handshape == "middle":  # zurück
            state = CONTROL_SELECT

    elif state == SHUTTER_CONTROL:
        if handshape == "thumb_up":
            control_shutter(selected_room, "up", current_user)
        elif handshape == "thumb_down":
            control_shutter(selected_room, "down", current_user)
        elif handshape == "fist":
            control_shutter(selected_room, "open", current_user)
        elif handshape == "pinky":
            control_shutter(selected_room, "close", current_user)
        elif handshape == "middle":  # zurück
            state = CONTROL_SELECT

    last_action_time = now
    return state, current_user, selected_room, handshape