import pygame
import config
from ui.base_widget import create_rooms
from vision.hand_tracking import (
    get_gesture_action,
    draw_help,
    USER_SELECT,
    ROOM_SELECT,
    CONTROL_SELECT,
    LIGHT_CONTROL,
    SHUTTER_CONTROL
)
# Steuerfunktionen nur für direkte Aufrufe (z.B. wenn nötig)
from ui.light_controller import control_light
from ui.shutter_controller import control_shutter

def main():
    pygame.init()

    # ----------------- Fenster -----------------
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)
    font = pygame.font.SysFont(None, config.FONT_SIZE)
    clock = pygame.time.Clock()

    # ----------------- Initialzustände -----------------
    current_user = config.DEFAULT_USER
    selected_room = None
    state = USER_SELECT  # <-- NEU: Startstate USER_SELECT
    rooms = create_rooms()  # Räume erzeugen

    running = True
    while running:

        # ----------------- Pygame Events -----------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ----------------- Gesten pro Frame -----------------
        state, current_user, selected_room, handshape = get_gesture_action(
            state, current_user, selected_room
        )

        # ----------------- UI Zeichnen -----------------
        screen.fill(config.BACKGROUND)  # Hintergrund zuerst

        # Räume zeichnen
        for room in rooms.values():
            room.draw(screen, font)

        # Overlay mit Gestenhinweisen
        draw_help(screen, font, state)

        # Aktueller Benutzer
        user_text = font.render(
            f"Aktueller Benutzer: {current_user or 'Nicht eingeloggt'}",
            True, (255, 255, 255))
        screen.blit(user_text, (20, 20))

        # Optional: Aktiver Raum anzeigen
        if selected_room:
            room_text = font.render(
                f"Aktiver Raum: {selected_room}",
                True, (255, 255, 0))
            screen.blit(room_text, (20, 60))

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
