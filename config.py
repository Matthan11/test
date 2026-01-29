# Hier kommen Konstanten und Einstellungen rein
# Modularisierung, Wartbarkeit, Saubere Struktur, Trennung von Logik & Konfiguration

import pygame
from ui.light_controller import dim_up, dim_down,toggle_light
from ui.shutter_controller import rollo_up, rollo_down, toggle_close

# Fenster
WIDTH = 800
HEIGHT = 600
FPS = 60
WINDOW_TITLE = "Schulaufgabe IT"

# Farben
WALL = (30, 30, 30)
FLOOR = (200, 190, 170)
WINDOW_COLOR = (180, 220, 255)
ROLLO = (120, 120, 120)
DARK = (0, 0, 0, 180)
BACKGROUND = (50, 50, 50)

# Schrift
FONT_SIZE = 36

# Benutzer
DEFAULT_USER = "user_a"

# -------------------------
# TASTENBELEGUNG
# -------------------------

KEYS = {
    # Raum 1 – Wohnküche
    pygame.K_q: ("room_1", rollo_up),
    pygame.K_a: ("room_1", rollo_down),
    pygame.K_y: ("room_1", toggle_close),
    pygame.K_w: ("room_1", dim_up),
    pygame.K_s: ("room_1", dim_down),
    pygame.K_x: ("room_1", toggle_light),

    # Raum 2 – Schlafzimmer 
    pygame.K_e: ("room_2", rollo_up),
    pygame.K_d: ("room_2", rollo_down),
    pygame.K_c: ("room_2", toggle_close),
    pygame.K_r: ("room_2", dim_up),
    pygame.K_f: ("room_2", dim_down),
    pygame.K_v: ("room_2", toggle_light),

    # Benutzer wechseln
    pygame.K_p: ("user", "user_a"),
    pygame.K_o: ("user", "user_b"),
}