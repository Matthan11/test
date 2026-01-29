import cv2
import mediapipe as mp
import time

# ================= MediaPipe Setup =================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ================= Status =================
room1 = {"light": 50, "blind": 50}
room2 = {"light": 50, "blind": 50}

USERS = {
    "Benutzer 1": "open",
    "Benutzer 2": "fist"
}

current_user = None
selected_room = None

last_gesture_time = 0
GESTURE_COOLDOWN = 1.2  # Sekunden

# ================= Hilfsfunktionen =================
def fingers_up(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Daumen
    fingers.append(
        1 if hand_landmarks.landmark[4].x <
             hand_landmarks.landmark[3].x else 0
    )

    # Andere Finger
    for i in [8, 12, 16, 20]:
        fingers.append(
            1 if hand_landmarks.landmark[i].y <
                 hand_landmarks.landmark[i - 2].y else 0
        )
    return fingers

def detect_handshape(f):
    if f == [0,0,0,0,0]:
        return "fist"
    if f == [1,1,1,1,1]:
        return "open"
    if f == [0,1,0,0,0]:
        return "index"
    if f == [0,1,1,0,0]:
        return "index_middle"
    if f == [1,0,0,0,0]:
        return "thumb_up"
    if f == [1,0,0,0,1]:
        return "thumb_down"
    if f == [0,0,1,0,0]:
        return "middle"
    return "other"

def change_light(room, delta, room_name):
    room["light"] = max(0, min(100, room["light"] + delta))
    print(f"Licht {room_name}: {room['light']}%")

def change_blind(room, delta, room_name):
    room["blind"] = max(0, min(100, room["blind"] + delta))
    print(f"Rollladen {room_name}: {room['blind']}%")

def draw_room(frame, room, name, x, y):
    cv2.putText(frame, name, (x, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)

    cv2.putText(frame, f"Licht: {room['light']}%", (x, y+30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    cv2.rectangle(frame, (x, y+45), (x+200, y+65), (50,50,50), -1)
    cv2.rectangle(frame, (x, y+45), (x+2*room['light'], y+65),
                  (0,255,255), -1)

    cv2.putText(frame, f"Rollladen: {room['blind']}%", (x, y+95),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.rectangle(frame, (x, y+110), (x+200, y+130), (50,50,50), -1)
    cv2.rectangle(frame, (x, y+110), (x+2*room['blind'], y+130),
                  (0,255,0), -1)

# ================= Hauptprogramm =================
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    now = time.time()

    if result.multi_hand_landmarks:
        for hand in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(hand)
            handshape = detect_handshape(fingers)

            # ===== LOGIN =====
            if current_user is None:
                for user, gesture in USERS.items():
                    if handshape == gesture and now - last_gesture_time > GESTURE_COOLDOWN:
                        current_user = user
                        print(f"{user} eingeloggt")
                        last_gesture_time = now

            # ===== RAUMAUSWAHL =====
            elif selected_room is None and now - last_gesture_time > GESTURE_COOLDOWN:
                if handshape == "index":
                    selected_room = "Raum 1"
                    print("Raum 1 ausgewählt")
                    last_gesture_time = now
                elif handshape == "thumb_up":
                    selected_room = "Raum 2"
                    print("Raum 2 ausgewählt")
                    last_gesture_time = now

            # ===== STEUERUNG =====
            elif now - last_gesture_time > GESTURE_COOLDOWN:
                room = room1 if selected_room == "Raum 1" else room2

                if handshape == "index_middle":
                    change_light(room, 20, selected_room)
                elif handshape == "middle":
                    change_light(room, -20, selected_room)
                elif handshape == "thumb_up":
                    change_blind(room, 25, selected_room)
                elif handshape == "thumb_down":
                    change_blind(room, -25, selected_room)

                last_gesture_time = now

    # ===== UI =====
    if current_user:
        cv2.putText(frame, f"Benutzer: {current_user}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    else:
        cv2.putText(frame, "Bitte einloggen", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,255), 2)

    if selected_room:
        cv2.putText(frame, f"Aktiver Raum: {selected_room}", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)
    else:
        cv2.putText(frame, "Raum auswaehlen", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    draw_room(frame, room1, "Raum 1", 10, 90)
    draw_room(frame, room2, "Raum 2", 10, 250)

    cv2.imshow("Gestensteuerung Smart Home", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
