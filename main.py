import pygame
import cv2
import mediapipe as mp

import config

# Avatare
from avatars import Avatar

# UI
from ui.base_widget import create_rooms

# State & Gesten
from vision.hand_tracking import (
    get_gesture_action,
    draw_help,
    USER_SELECT,
    ROOM_SELECT,
    CONTROL_SELECT,
    LIGHT_CONTROL,
    SHUTTER_CONTROL
)

# ================= INITIALISIERUNG =================

# Pygame starten
pygame.init()

# Fenster erstellen
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption(config.WINDOW_TITLE)

# Schrift & Clock
font = pygame.font.SysFont(None, config.FONT_SIZE)
clock = pygame.time.Clock()

# ================= KAMERA =================

# Kamera wird NUR HIER geöffnet (sehr wichtig!)
cap = cv2.VideoCapture(0)

# ================= STARTZUSTÄNDE =================

state = USER_SELECT        # Start im User-Auswahlmodus
current_user = None        # Kein Benutzer eingeloggt
selected_room = None       # Kein Raum gewählt

# Räume erzeugen
rooms = create_rooms()

# ================= AVATARE =================

user1_avatar = Avatar(
    name="User 1",
    color=(0, 160, 255),
    position=(120, 140),
    style="hair"
)

user2_avatar = Avatar(
    name="User 2",
    color=(255, 120, 0),
    position=(280, 140),
    style="cap"
)

avatars = {
    "User 1": user1_avatar,
    "User 2": user2_avatar
}


# ================= HAUPTSCHLEIFE =================

running = True
while running:

    # ---------- EVENTS ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ---------- KAMERALESEN ----------
    ret, frame = cap.read()

    if ret:
        # Übergabe des aktuellen Frames an die State-Machine
        state, current_user, selected_room, handshape = get_gesture_action(
            state,
            current_user,
            selected_room,
            frame,
            rooms,
        )
    # === AKTIVEN AVATAR SETZEN ===
    for avatar in avatars.values():
        avatar.active = False

    if current_user in avatars:
        avatars[current_user].active = True

    # ---------- HINTERGRUND ----------
    screen.fill(config.BACKGROUND)

    # ---------- RÄUME ZEICHNEN ----------
    for room in rooms.values():
        room.draw(screen, font)

    # ---------- HILFE-OVERLAY ----------
    draw_help(screen, font, state)

    # ---------- STATUSANZEIGE ----------
    user_text = font.render(
        f"Current user: {current_user or '---'}",
        True,
        (255, 255, 255)
    )
    screen.blit(user_text, (20, 20))

    if selected_room:   # Statusanzeige Raum
        room_text = font.render(
            f"Current room: {selected_room.name}",
            True,
            (255, 255, 255)
        )
        screen.blit(room_text, (20, 60))

    #---------- AVATARE ZEICHNEN ----------
    for avatar in avatars.values():
        avatar.draw(screen, font)

    # ---------- LIVE-KAMERABILD ----------
    if ret:
        # Kamera verkleinern
        preview = cv2.resize(frame, (320, 240))
        preview = cv2.cvtColor(preview, cv2.COLOR_BGR2RGB)

        # OpenCV → Pygame Surface
        preview_surface = pygame.surfarray.make_surface(preview.swapaxes(0, 1))
        screen.blit(preview_surface, (config.WIDTH - 330, 10))

    # ---------- UPDATE ----------
    pygame.display.flip()
    clock.tick(config.FPS)

# ================= AUFRÄUMEN =================

cap.release()
pygame.quit()
