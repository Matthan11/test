import cv2
import mediapipe as mp
import time

# ===== MediaPipe Setup =====
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ===== Status von Licht und Rollläden =====
room1 = {"light": 0, "blind": 0}
room2 = {"light": 0, "blind": 0}

# ===== Benutzer Login Gesten =====
# "open" = offene Hand, "fist" = Faust
USERS = {
    "Benutzer1": "open",
    "Benutzer2": "fist"
}

current_user = None
last_gesture_time = 0
GESTURE_COOLDOWN = 1.0  # Sekunden

# ===== Funktionen =====
def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []
    # Daumen
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    # Zeigefinger, Mittelfinger, Ringfinger, kleiner Finger
    for id in range(1,5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id]-2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers

def detect_handshape(fingers):
    """Erkennt einfache Handformen, ohne Ringfinger zu nutzen"""
    # Faust
    if fingers == [0,0,0,0,0]:
        return "fist"
    # Offene Hand
    elif fingers == [1,1,1,1,1]:
        return "open"
    # Zeigefinger
    elif fingers == [0,1,0,0,0]:
        return "index"
    # Zeigefinger + Mittelfinger
    elif fingers == [0,1,1,0,0]:
        return "index_middle"
    # Daumen hoch
    elif fingers == [1,0,0,0,0]:
        return "thumb_up"
    # Daumen runter (Daumen nach unten, andere Finger geschlossen)
    elif fingers == [1,0,0,0,1]:  # kleiner Finger als Orientierung
        return "thumb_down"
    # Mittelfinger
    elif fingers == [0,0,1,0,0]:
        return "middle"
    # Kleiner Finger
    elif fingers == [0,0,0,0,1]:
        return "pinky"
    else:
        return "other"

def change_light(room, delta, room_name):
    room["light"] = min(max(room["light"] + delta, 0), 100)
    print(f"Licht in {room_name}: {room['light']}%")

def change_blind(room, delta, room_name):
    room["blind"] = min(max(room["blind"] + delta, 0), 100)
    print(f"Rollladen in {room_name}: {room['blind']}% geöffnet")

def draw_status(frame, room, room_name, x, y):
    cv2.putText(frame, f"{room_name}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
    # Lichtbalken
    cv2.putText(frame, f"Licht: {room['light']}%", (x, y+30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    cv2.rectangle(frame, (x, y+50), (x+200, y+70), (50,50,50), -1)
    cv2.rectangle(frame, (x, y+50), (x+2*room['light'], y+70), (0,255,255), -1)
    # Rollladenbalken
    cv2.putText(frame, f"Rollladen: {room['blind']}%", (x, y+100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.rectangle(frame, (x, y+120), (x+200, y+140), (50,50,50), -1)
    cv2.rectangle(frame, (x, y+120), (x+2*room['blind'], y+140), (0,255,0), -1)

# ===== Hauptprogramm =====
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    now = time.time()

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(hand_landmarks)
            handshape = detect_handshape(fingers)

            # ===== Login =====
            if current_user is None:
                for user, gesture in USERS.items():
                    if handshape == gesture and now - last_gesture_time > GESTURE_COOLDOWN:
                        current_user = user
                        print(f"{current_user} erfolgreich eingeloggt!")
                        last_gesture_time = now

            # ===== Steuerung Raum 1 =====
            elif now - last_gesture_time > GESTURE_COOLDOWN:
                # Raum 1
                if handshape == "index":
                    change_light(room1, 20, "Raum 1")
                elif handshape == "index_middle":
                    change_light(room1, -20, "Raum 1")
                elif handshape == "thumb_up":
                    change_blind(room1, 25, "Raum 1")
                elif handshape == "thumb_down":
                    change_blind(room1, -25, "Raum 1")

                # Raum 2
                elif handshape == "pinky":
                    change_light(room2, 20, "Raum 2")
                elif handshape == "middle":
                    change_light(room2, -20, "Raum 2")
                elif handshape == "index_middle":
                    change_blind(room2, 25, "Raum 2")
                elif handshape == "fist":
                    change_blind(room2, -25, "Raum 2")

                last_gesture_time = now

    # ===== Anzeige =====
    if current_user:
        cv2.putText(frame, f"Benutzer: {current_user}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
    else:
        cv2.putText(frame, "Login: Benutzer Geste zeigen", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    draw_status(frame, room1, "Raum 1", 10, 60)
    draw_status(frame, room2, "Raum 2", 10, 220)

    cv2.imshow("Gesten Home Control", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()