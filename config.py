import pygame
from logging_system import write_log

pygame.init()

# Fenster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schulaufgabe IT")
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Farben
WALL = (30, 30, 30)
FLOOR = (200, 190, 170)
WINDOW = (180, 220, 255)
ROLLO = (120, 120, 120)
DARK = (0, 0, 0, 180)

current_user = "user_a"

# Raum-Klasse
class Room:
    def __init__(self, rect, window_rect, name):
        self.rect = rect
        self.window = window_rect
        self.light_on = True
        self.rollo_height = 0
        self.name = name

    def toggle_light(self, user):
        self.light_on = not self.light_on
        action = f"{self.name}: Licht {'AN' if self.light_on else 'AUS'}"
        write_log(user, action)

    def rollo_up(self, user):
        self.rollo_height = max(0, self.rollo_height - 5)
        write_log(user, f"{self.name}: Rollo hoch")

    def rollo_down(self, user):
        self.rollo_height = min(self.window.height, self.rollo_height + 5)
        write_log(user, f"{self.name}: Rollo runter")

    def draw(self, surface):
        pygame.draw.rect(surface, FLOOR, self.rect)
        pygame.draw.rect(surface, WALL, self.rect, 4)

        pygame.draw.rect(surface, WINDOW, self.window)

        rollo_rect = pygame.Rect(
            self.window.x,
            self.window.y,
            self.window.width,
            self.rollo_height
        )
        pygame.draw.rect(surface, ROLLO, rollo_rect)

        if not self.light_on:
            dark = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            dark.fill(DARK)
            surface.blit(dark, self.rect.topleft)


# Räume korrekt erzeugen
room_1 = Room(
    pygame.Rect(50, 50, 700, 230),
    pygame.Rect(100, 60, 150, 50),
    "Wohnküche"
)

room_2 = Room(
    pygame.Rect(50, 280, 700, 220),
    pygame.Rect(60, 310, 50, 150),
    "Schlafzimmer"
)


# Hauptloop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Raum 1
            if event.key == pygame.K_1:
                room_1.toggle_light(current_user)
            if event.key == pygame.K_q:
                room_1.rollo_up(current_user)
            if event.key == pygame.K_a:
                room_1.rollo_down(current_user)

            # Raum 2
            if event.key == pygame.K_2:
                room_2.toggle_light(current_user)
            if event.key == pygame.K_w:
                room_2.rollo_up(current_user)
            if event.key == pygame.K_s:
                room_2.rollo_down(current_user)

            # Benutzer wechseln
            if event.key == pygame.K_p:
                current_user = "user_a"
                write_log(current_user, "Benutzer gewechselt zu user_a")

            if event.key == pygame.K_o:
                current_user = "user_b"
                write_log(current_user, "Benutzer gewechselt zu user_b")

    # Bildschirm JEDEN FRAME neu zeichnen
    screen.fill((50, 50, 50))
    room_1.draw(screen)
    room_2.draw(screen)

    # Benutzer anzeigen
    user_text = font.render(f"Aktueller Benutzer: {current_user}", True, (255, 255, 255))
    screen.blit(user_text, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
