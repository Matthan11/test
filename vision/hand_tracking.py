import cv2
import mediapipe as mp
import time

# Steuerungsmodule
from ui.control_light import control_light
from ui.control_shutter import control_shutter
from logging_system import write_log

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
    Gibt eine Liste mit 5 Werten zurück (Daumen --> kleiner Finger)
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
    
    if f == [1,0,1,0,1]:    # Daumen, Mittel- und Kleinerfinger
        return "thumb_middle_pinky"

    return "other"


# ================= Overlay =================
def draw_help(screen, font, state):
    """
    Zeichnet die Hilfe-Anzeige rechts unten im Fenster
    """
    x, y = 850, 400

    # Bentzer auswahl
    if state == USER_SELECT:
        lines = [
            "USER SELECT:",
            "Indexfinger --> User 1",                           # user_1
            "Index- + Middlefinger --> User 2"                  # user_2
        ]
    
    # Raum auswahl
    elif state == ROOM_SELECT:
        lines = [
            "ROOM SELECT:",
            "Indexfinger                    --> Kitchen",           # Weiter zu room_1
            "Index- + Middlefinger          --> Sleepingroom",      # Weiter zu room_2
            "Thumb + Middle- + Pinkyfinger  --> Return"             # Zurück zu USER_SELECT
        ]

    # Steuerungs auswahl
    elif state == CONTROL_SELECT:
        lines = [
            "CONTROL:",
            "Index                  --> Light",                     # Weiter zu control_light
            "Index- + Middlefinger  --> Shutter",                   # Weiter zu control_shutter
            "Thumb + Middlefinger   --> Return"                     # Zurück zu ROOM_SELECT
        ]

    elif state == LIGHT_CONTROL:
        lines = [
            "LIGHT CONTROL:",
            "Index                  --> Dim the light brighter",    # Licht heller dimmen
            "Index- + Middlefinger  --> Dim the light darker",      # Licht dunkler dimmen
            "Open (allfingers)      --> Light completely off",      # Licht komplett ausschalten
            "Pinky                  --> Lights completely on",      # Licht komplett anschalten
            "Middlefinger --> Retrun"                               # Zurück zu CONTROL_SELECT
        ]

    elif state == SHUTTER_CONTROL:
        lines = [
            "SHUTTER CONTROL:",
            "Index                  --> raise the Shutter",         # Rollo öffnen
            "Index- + Middlefinger  --> close the Shutter",         # Rollo schließen
            "Open (allfingers)      --> Shutter completely open",   # Rollo komplett öffnen
            "Pinky                  --> Shutter completely closed", # Rollo komplett schließen
            "Middlefinger           --> Return"                     # Zurück zu CONTROL_SELECT
        ]

    else:
        lines = ["Unknown State"]

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

    # Kein Bild --> nichts tun
    if frame is None:
        return state, current_user, selected_room, None

    # Bild spiegeln (natürliche Bewegung)
    frame = cv2.flip(frame, 1)

    # In RGB umwandeln (MediaPipe erwartet RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    now = time.time()
    # Cooldown aktiv → nichts tun
    if now - last_action_time < COOLDOWN:
        return state, current_user, selected_room, None

    # Keine Hand oder Cooldown aktiv --> nichts tun
    if not result.multi_hand_landmarks:
        return state, current_user, selected_room, None

    # Erste erkannte Hand verwenden
    hand = result.multi_hand_landmarks[0]
    hand_label = result.multi_handedness[0].classification[0].label  # 'Left' oder 'Right'

    # Geste erk
    f = fingers_up(hand)

    # Daumen horizontal korrigieren je nach Hand
    if hand_label == "Right":
        f[0] = 1 if hand.landmark[4].x < hand.landmark[3].x else 0
    else:
        f[0] = 1 if hand.landmark[4].x > hand.landmark[3].x else 0

    handshape = detect_handshape(f, hand)




    action_taken = False  # Tracken, ob wir etwas tun -> Cooldown setzen

    # ================= STATE MACHINE =================
    if state == USER_SELECT:
        if handshape == "index":
            current_user = "User 1"
            write_log(current_user, f"login {current_user}")
            state = ROOM_SELECT
            action_taken = True
        elif handshape == "index_middle":
            current_user = "User 2"
            write_log(current_user, f"login {current_user}")
            state = ROOM_SELECT
            action_taken = True

    elif state == ROOM_SELECT:
        if handshape == "index":
            selected_room = rooms.get("room_1")
            write_log(current_user, f"{current_user} selected {selected_room.name}")
            state = CONTROL_SELECT
            action_taken = True

        elif handshape == "index_middle":
            selected_room = rooms.get("room_2")
            write_log(current_user, f"{current_user} selected {selected_room.name}")
            state = CONTROL_SELECT
            action_taken = True

        elif handshape == "thumb_middle_pinky":
            write_log(current_user, f"{current_user} returned to USER_SELECT")
            state = USER_SELECT
            current_user = None
            selected_room = None
            action_taken = True

    elif state == CONTROL_SELECT:
        if handshape == "index":
            state = LIGHT_CONTROL
            action_taken = True
        elif handshape == "index_middle":
            state = SHUTTER_CONTROL
            action_taken = True
        elif handshape == "thumb_middle":
            state = ROOM_SELECT
            selected_room = None
            action_taken = True

    elif state == LIGHT_CONTROL:
        if handshape == "index":
            control_light(selected_room, "up", current_user)
            action_taken = True
        elif handshape == "index_middle":
            control_light(selected_room, "down", current_user)
            action_taken = True
        elif handshape == "open":
            control_light(selected_room, "off", current_user)
            action_taken = True
        elif handshape == "pinky":
            control_light(selected_room, "on", current_user)
            action_taken = True
        elif handshape == "middle":
            state = CONTROL_SELECT
            action_taken = True

    elif state == SHUTTER_CONTROL:
        if handshape == "index":
            control_shutter(selected_room, "up", current_user)
            action_taken = True
        elif handshape == "index_middle":
            control_shutter(selected_room, "down", current_user)
            action_taken = True
        elif handshape == "open":
            control_shutter(selected_room, "open", current_user)
            action_taken = True
        elif handshape == "pinky":
            control_shutter(selected_room, "close", current_user)
            action_taken = True
        elif handshape == "middle":
            state = CONTROL_SELECT
            action_taken = True

    # Cooldown nur setzen, wenn tatsächlich eine Aktion ausgeführt wurde
    if action_taken:
        last_action_time = now

    return state, current_user, selected_room, handshape
