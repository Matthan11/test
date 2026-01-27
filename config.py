import pygame

# Fenster
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Schulaufgabe IT")

lock = pygame.time.Clock()

# Farben
WALL = (30, 30, 30)
FLOOR = (200, 190, 170)
WINDOW = (180, 220, 255)
ROLLO = (120, 120, 120)
DARK = (0, 0, 0, 180)

pygame.quit()
