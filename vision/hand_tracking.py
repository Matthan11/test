import cv2
import mediapipe as mp
import time

# Steuerungsmodule
from ui.light_controller import control_light
from ui.shutter_controller import control_shutter

# ================= MediaPipe =================
# Initialisierung der Handerkennung (KEINE Kamera hier!)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,                  # Nur eine Hand erkennen
    min_detection_confidence=0.7,     # Mindest-Erkennungswahrscheinlichkeit
    min_tracking_confidence=0.7       # Mindest-Tracking-Stabilität
)

# ================= STATES =================
# Zustände der State-Machine
USER_SELECT = "user_select"
ROOM_SELECT = "room_select"
CONTROL_SELECT = "control_select"
LIGHT_CONTROL = "light_control"
SHUTTER_CONTROL = "shutter_control"

# Cooldown gegen Mehrfachauslösung
COOLDOWN = 1.2
last_action_time = 0


# ================= Finger-Erkennung =================
def fingers_up(hand):
    """
    Gibt eine Liste mit 5 Werten zurück (Daumen → kleiner Finger)
    1 = Finger oben, 0 = Finger unten
    """
    fingers = []

    # Daumen (horizontal)
    fingers.append(1 if hand.landmark[4].x < hand.landmark[3].x else 0)

    # Andere Finger (vertikal)
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0)

    return fingers


# ================= Handshape-Erkennung =================
def detect_handshape(f, hand=None):
    """
    Wandelt Finger-Muster in eine Geste um
    """
    if f == [0,0,0,0,0]:    # Faust
        return "fist"

    if f == [1,1,1,1,1]:    # Alle Finger
        return "open"
    if f == [1,0,0,0,0]:    # Daumen
        if hand and hand.landmark[4].y > hand.landmark[2].y:
            return "thumb_down" # Daumen runter
        else:
            return "thumb_up"   # Daumen hoch

    if f == [0,1,0,0,0]:    # Zeigefinger
        return "index"

    if f == [0,1,1,0,0]:    # Zeigefinger und Mittelfinger
        return "index_middle"

    if f == [0,0,1,0,0]:    # Mittelfinger
        return "middle"

    if f == [0,0,0,0,1]:    # Kleinerfinger
        return "pinky"

    if f == [1,0,1,0,0]:    # Daumen und Mittelfinger
        return "thumb_middle"

    return "other"


# ================= Overlay =================
def draw_help(screen, font, state):
    """
    Zeichnet die Hilfe-Anzeige rechts unten im Fenster
    """
    x, y = 850, 400

    if state == USER_SELECT:
        lines = [
            "USER WAHL:",
            "Zeigefinger → User 1",
            "Zeige- & Mittelfinger → User 2"
        ]

    elif state == ROOM_SELECT:
        lines = [
            "RAUM WAHL:",
            "Zeigefinger → Raum 1",
            "Zeige- & Mittelfinger → Raum 2",
            "Daumen und Mittelfinger → Zurück"
        ]

    elif state == CONTROL_SELECT:
        lines = [
            "STEUERUNG:",
            "Zeigefinger → Licht",
            "Zeige- & Mittelfinger → Rollo",
            "Mittelfinger → Zurück"
        ]

    elif state == LIGHT_CONTROL:
        lines = [
            "LICHT:",
            "Daumen hoch → Heller",
            "Daumen runter → Dunkler",
            "Alle Finger → Licht komplett aus",
            "Kleinerfinger → Licht komplett an",
            "Mittelfinger → Zurück"
        ]

    elif state == SHUTTER_CONTROL:
        lines = [
            "ROLLO:",
            "Daumen hoch → Rollo hoch",
            "Daumen runter → Rollo runter",
            "Alle Finger → Rollo komplett auf",
            "Kleinerfinger → Rollo komplett zu",
            "Mittelfinger → Zurück"
        ]

    else:
        lines = ["Unbekannter State"]

    for line in lines:
        txt = font.render(line, True, (255, 255, 255))
        screen.blit(txt, (x, y))
        y += 30


# ================= State-Machine =================
def get_gesture_action(state, current_user, selected_room, frame, rooms):
    """
    Zentrale Zustandslogik
    frame kommt aus main (keine Kamera hier!)
    """
    global last_action_time

    # Bild spiegeln (natürliche Bewegung)
    frame = cv2.flip(frame, 1)

    # In RGB umwandeln (MediaPipe erwartet RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    now = time.time()

    # Keine Hand oder Cooldown aktiv → nichts tun
    if not result.multi_hand_landmarks or now - last_action_time < COOLDOWN:
        return state, current_user, selected_room, None

    # Erste erkannte Hand verwenden
    hand = result.multi_hand_landmarks[0]

    # Geste erkennen
    handshape = detect_handshape(fingers_up(hand), hand)

    # ================= STATE MACHINE =================
    if state == USER_SELECT:
        if handshape == "index":
            current_user = "User 1"
            state = ROOM_SELECT
        elif handshape == "index_middle":
            current_user = "User 2"
            state = ROOM_SELECT

    elif state == ROOM_SELECT:
        if handshape == "index":
            selected_room = rooms["room_1"]   # <-- Objekt
            state = CONTROL_SELECT

        elif handshape == "index_middle":
            selected_room = rooms["room_2"]   # <-- Objekt
            state = CONTROL_SELECT

        elif handshape in ("thumb_middle"):
            state = USER_SELECT
            current_user = None
            selected_room = None

    elif state == CONTROL_SELECT:
        if handshape == "index":
            state = LIGHT_CONTROL
        elif handshape == "index_middle":
            state = SHUTTER_CONTROL
        elif handshape == "middle":
            state = ROOM_SELECT
            selected_room = None

    elif state == LIGHT_CONTROL:
        if handshape == "thumb_up":
            control_light(selected_room, "up", current_user)
        elif handshape == "thumb_down":
            control_light(selected_room, "down", current_user)
        elif handshape == "open":
            control_light(selected_room, "off", current_user)
        elif handshape == "pinky":
            control_light(selected_room, "on", current_user)
        elif handshape == "middle":
            state = CONTROL_SELECT

    elif state == SHUTTER_CONTROL:
        if handshape == "thumb_up":
            control_shutter(selected_room, "up", current_user)
        elif handshape == "thumb_down":
            control_shutter(selected_room, "down", current_user)
        elif handshape == "open":
            control_shutter(selected_room, "open", current_user)
        elif handshape == "pinky":
            control_shutter(selected_room, "close", current_user)
        elif handshape == "middle":
            state = CONTROL_SELECT

    # Cooldown-Zeit merken
    last_action_time = now

    return state, current_user, selected_room, handshape
