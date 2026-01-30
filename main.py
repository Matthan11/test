import pygame
import cv2
import mediapipe as mp
import time

import config
from ui.base_widget import create_rooms
from ui.light_controller import control_light
from ui.shutter_controller import control_shutter
from vision.hand_tracking_neu import (
    get_gesture_action,
    draw_help,
    USER_SELECT,
    ROOM_SELECT,
    CONTROL_SELECT,
    LIGHT_CONTROL,
    SHUTTER_CONTROL,
    detect_handshape,
    fingers_up
)

# ----------------- Kamera für Live-Feed -----------------
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# ----------------- Main-Funktion -----------------
def main():
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    font = pygame.font.SysFont(None, config.FONT_SIZE)
    clock = pygame.time.Clock()

    # ----------------- Initialzustände -----------------
    current_user = config.DEFAULT_USER
    selected_room = None
    state = USER_SELECT
    rooms = create_rooms()
    last_action_time = 0
    COOLDOWN = 1.0  # Sekunden

    running = True
    while running:
        # -------- Pygame Events --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------- Kamera lesen & Gesten erkennen --------
        ret, frame = cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            handshape = None
            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                handshape = detect_handshape(fingers_up(hand), hand)
                now = time.time()
                if now - last_action_time > COOLDOWN:
                    # State-Maschine
                    state, current_user, selected_room, _ = get_gesture_action(
                        state, current_user, selected_room
                    )
                    last_action_time = now

        # -------- UI Zeichnen --------
        screen.fill(config.BACKGROUND)

        # ----------------- State-Hervorhebung -----------------
        state_colors = {
            USER_SELECT: (0, 255, 0),        # grün
            ROOM_SELECT: (255, 255, 0),      # gelb
            CONTROL_SELECT: (0, 255, 255),   # cyan
            LIGHT_CONTROL: (255, 0, 0),      # rot
            SHUTTER_CONTROL: (0, 0, 255)     # blau
        }
        pygame.draw.rect(screen, state_colors.get(state, (255, 255, 255)), (10, 10, 200, 50))

        # ----------------- Räume -----------------
        for room in rooms.values():
            room.draw(screen, font)

        # ----------------- Overlay -----------------
        draw_help(screen, font, state)

        # ----------------- Aktueller Benutzer & Raum -----------------
        user_text = font.render(f"Aktueller Benutzer: {current_user or 'Nicht eingeloggt'}",
                                True, (255, 255, 255))
        screen.blit(user_text, (20, 20))

        if selected_room:
            room_text = font.render(f"Aktiver Raum: {selected_room}",
                                    True, (255, 255, 0))
            screen.blit(room_text, (20, 60))

        # ----------------- Aktuelle erkannte Geste -----------------
        gesture_text = font.render(f"Geste erkannt: {handshape or 'keine'}",
                                   True, (0, 255, 255))
        screen.blit(gesture_text, (20, 90))

        # ----------------- Live-Kamera-Vorschau -----------------
        if ret:
            frame_small = cv2.resize(frame, (320, 240))
            frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
            screen.blit(frame_surface, (config.WIDTH - 330, 10))  # rechts oben

        pygame.display.flip()
        clock.tick(config.FPS)

    # -------- Cleanup --------
    cap.release()
    pygame.quit()


if __name__ == "__main__":
    main()