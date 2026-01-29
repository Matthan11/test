import cv2
import mediapipe as mp
import time

from login import handle_login
from room_selection import handle_room_selection
from control import control_light, control_blind

# ================= MediaPipe =================
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# ================= Status =================
room1 = {"light": 50, "blind": 50}
room2 = {"light": 50, "blind": 50}

current_user = None
selected_room = None

last_action_time = 0
COOLDOWN = 1.2

# ================= Finger-Erkennung =================
def fingers_up(hand):
    tips = [4, 8, 12, 16, 20]
    fingers = []

    # Daumen
    fingers.append(1 if hand.landmark[4].x < hand.landmark[3].x else 0)

    # Andere Finger
    for tip in [8, 12, 16, 20]:
        fingers.append(1 if hand.landmark[tip].y < hand.landmark[tip - 2].y else 0)

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
    if f == [1,1,0,0,0]:
        return "thumb_index"
    if f == [0,0,1,0,0]:
        return "middle"
    if f == [0,0,0,0,1]:
        return "pinky"
    return "other"

# ================= Anzeige =================
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

# ================= Hauptloop =================
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
            handshape = detect_handshape(fingers_up(hand))

            if now - last_action_time > COOLDOWN:
                current_user = handle_login(handshape, current_user)
                selected_room = handle_room_selection(handshape, selected_room)

                if current_user and selected_room:
                    room = room1 if selected_room == "Raum 1" else room2
                    control_light(room, handshape)
                    control_blind(room, handshape)

                last_action_time = now

    # UI
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

    draw_room(frame, room1, "Raum 1", 10, 100)
    draw_room(frame, room2, "Raum 2", 10, 260)

    cv2.imshow("Gesten Smart Home", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
