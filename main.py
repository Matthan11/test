
import pygame
import config
from ui.base_widget import create_rooms
from logging_system import write_log

def main():
    pygame.init()

    # Fenster
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.WINDOW_TITLE)

    font = pygame.font.SysFont(None, config.FONT_SIZE)
    clock = pygame.time.Clock()

    current_user = config.DEFAULT_USER

    # Räume erzeugen
    rooms = create_rooms()

    # Hauptloop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key in config.KEYS:
                target, action = config.KEYS[event.key]

                # Raum-Aktionen
                if target in rooms:
                    getattr(rooms[target],action)(current_user)

            # Benutzer wechseln
                elif target == "user":
                    current_user = action
                    write_log(current_user, f"Benutzer gewechselt zu {current_user}")

        # Bildschirm JEDEN FRAME neu zeichnen
        screen.fill(config.BACKGROUND)
        for room in rooms.values():
            room.draw(screen)

        # Benutzer anzeigen
        user_text = font.render(f"Aktueller Benutzer: {current_user}", True, (255, 255, 255))
        screen.blit(user_text, (20, 20))

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()



if __name__ == "__main__":
    main()