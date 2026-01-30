# Hier kommen Konstanten und Einstellungen rein
# Modularisierung, Wartbarkeit, Saubere Struktur, Trennung von Logik & Konfiguration

# import pygame
# from ui.light_controller import dim_up, dim_down,toggle_light
# from ui.shutter_controller import rollo_up, rollo_down, toggle_close

# Fenster
WIDTH = 1200
HEIGHT = 700
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
DEFAULT_USER = None

def clamp(value):
    return max(0, min(100, value))