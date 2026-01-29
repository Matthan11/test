# Erzeugen des Raumes



import pygame
from logging_system import write_log
import config

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
        pygame.draw.rect(surface, config.FLOOR, self.rect)
        pygame.draw.rect(surface, config.WALL, self.rect, 4)

        pygame.draw.rect(surface, config.WINDOW_COLOR, self.window)

        rollo_rect = pygame.Rect(
            self.window.x,
            self.window.y,
            self.window.width,
            self.rollo_height
        )
        pygame.draw.rect(surface, config.ROLLO, rollo_rect)

        if not self.light_on:
            dark = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            dark.fill(config.DARK)
            surface.blit(dark, self.rect.topleft)

# ----------------------------------
# RÄUME ERZEUGEN
# ----------------------------------

def create_rooms():
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

    return {
        "room_1": room_1,
        "room_2": room_2
    }     
