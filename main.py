import pygame
import config
from ui.base_widget import create_rooms
from vision.hand_tracking_neu import get_gesture_action
from ui.light_controller import control_light
from ui.shutter_controller import control_shutter

def main():
    pygame.init()

    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)

    font = pygame.font.SysFont(None, config.FONT_SIZE)
    clock = pygame.time.Clock()

    current_user = config.DEFAULT_USER
    selected_room = None

    rooms = create_rooms()

    running = True
    while running:

        # -------- Pygame Events --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # -------- Gesten (pro Frame!) --------
        current_user, selected_room, handshape = get_gesture_action(
            current_user, selected_room
        )

        if handshape and selected_room:
            room = rooms.get(selected_room)

            if room:
                control_light(room, handshape, current_user)
                control_shutter(room, handshape, current_user)

        # -------- UI --------
        screen.fill(config.BACKGROUND)

        for room in rooms.values():
            room.draw(screen, font)

        user_text = font.render(
            f"Aktueller Benutzer: {current_user}", True, (255, 255, 255))
        screen.blit(user_text, (20, 20))

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()