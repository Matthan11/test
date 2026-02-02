# Erstellt von Jannik Langhammer
# Erzeugen des Raumes

import pygame
import config as config


# ================= RAUM-KLASSE =================
class Room:
    def __init__(self, rect, window_rect, name):
        self.rect = rect                    # Raumrechteck
        self.window = window_rect           # Fensterrechteck
        self.rollo_height = 0               # Rollo-Höhe (Pixel)
        self.name = name                    # Raumname
        self.light_level = 0                # Lichtstärke in Prozent

    def draw(self, surface, font):

        # ================= LICHTSTEUERUNG =================
        factor = self.light_level / 100     # Faktor 0.0 – 1.0

        floor_color = (
            int(config.FLOOR[0] * factor),
            int(config.FLOOR[1] * factor),
            int(config.FLOOR[2] * factor),
        )

        # Boden und Wände zeichnen
        pygame.draw.rect(surface, floor_color, self.rect)
        pygame.draw.rect(surface, config.WALL, self.rect, 4)

        # Fenster zeichnen
        pygame.draw.rect(surface, config.WINDOW_COLOR, self.window)

        # ================= MÖBEL =================
        if self.name == "Sleepingroom":
            self._draw_wardrobe(surface)    # Schrank oben links
            self._draw_bed(surface)         # Bett mittig

        if self.name == "Kitchen":
            self._draw_kitchen(surface)     # Küchenzeile am Fenster
            self._draw_couch(surface)       # Couch gegenüber Fenster

        # ================= LICHTANZEIGE =================
        light_text = font.render(
            f"Licht: {self.light_level}%",
            True,
            (255, 0, 0)
        )
        surface.blit(
            light_text,
            (self.rect.right - light_text.get_width() - 10, self.rect.y + 10)
        )

        # ================= ROLLO =================
        rollo_rect = pygame.Rect(
            self.window.x,
            self.window.y,
            self.window.width,
            self.rollo_height
        )

        pygame.draw.rect(surface, config.ROLLO, rollo_rect)

        percent = int((self.rollo_height / self.window.height) * 100)
        percent_text = font.render(f"{percent}%", True, (255, 0, 0))

        surface.blit(
            percent_text,
            (
                self.window.right + 10,
                self.window.y + self.window.height // 2 - percent_text.get_height() // 2
            )
        )

        # ================= TÜR =================
        self.draw_door(surface)

    # ================= MÖBEL =================

    def _draw_bed(self, surface):
        # Bett mittig im Schlafzimmer
        bed_width = 140
        bed_height = 70

        bed_rect = pygame.Rect(
            self.rect.centerx - bed_width // 2,
            self.rect.centery - bed_height // 2,
            bed_width,
            bed_height
        )

        pygame.draw.rect(surface, (180, 180, 200), bed_rect)
        pygame.draw.rect(surface, (120, 120, 160), bed_rect, 3)

        # Kopfkissen
        pillow = pygame.Rect(bed_rect.x + 10, bed_rect.y + 10, 40, 20)
        pygame.draw.rect(surface, (230, 230, 230), pillow)

    def _draw_wardrobe(self, surface):
        # Schrank linke obere Ecke
        wardrobe_rect = pygame.Rect(
            self.rect.x + 20,
            self.rect.y + 20,
            90,
            140
        )

        pygame.draw.rect(surface, (120, 80, 40), wardrobe_rect)
        pygame.draw.rect(surface, (80, 50, 20), wardrobe_rect, 3)

        # Schranktüren
        pygame.draw.line(
            surface,
            (60, 40, 20),
            wardrobe_rect.midtop,
            wardrobe_rect.midbottom,
            2
        )

    def _draw_kitchen(self, surface):
        # Küchenzeile direkt neben dem Fenster
        kitchen_rect = pygame.Rect(
            self.window.right + 100,
            self.window.y,
            180,
            50
        )

        pygame.draw.rect(surface, (160, 160, 160), kitchen_rect)
        pygame.draw.rect(surface, (100, 100, 100), kitchen_rect, 3)

        # Kochfelder
        pygame.draw.circle(surface, (50, 50, 50), (kitchen_rect.x + 50, kitchen_rect.y + 25), 8)
        pygame.draw.circle(surface, (50, 50, 50), (kitchen_rect.x + 90, kitchen_rect.y + 25), 8)

    def _draw_couch(self, surface):
        # Couch gegenüber vom Fenster (unten im Raum)
        couch_rect = pygame.Rect(
            self.rect.centerx - 300,
            self.rect.bottom - 80,
            160,
            60
        )

        pygame.draw.rect(surface, (100, 60, 60), couch_rect)
        pygame.draw.rect(surface, (70, 40, 40), couch_rect, 3)

        # Rückenlehne AUF DER ANDEREN SEITE (unten)
        backrest = pygame.Rect(
            couch_rect.x,
            couch_rect.bottom,
            couch_rect.width,
            18
        )

        pygame.draw.rect(surface, (120, 70, 70), backrest)

    def draw_door(self, surface):
        # Tür mittig rechts in der Küche
        if self.name == "Kitchen":
            door_height = 60

            door_rect = pygame.Rect(
                self.rect.right - 4,
                self.rect.centery - door_height // 2,
                8,
                door_height
            )

        # Tür zwischen beiden Räumen
        if self.name == "Sleepingroom":

            door_width = 60

            door_rect = pygame.Rect(
                self.rect.centerx - door_width // 2,
                self.rect.y - 4,
                door_width,
                8
            )

        pygame.draw.rect(surface, (160, 160, 160), door_rect)


# ================= RÄUME ERZEUGEN =================

def create_rooms():
    room_1 = Room(
        pygame.Rect(50, 100, 700, 230),
        pygame.Rect(100, 110, 150, 50),
        "Kitchen"
    )

    room_2 = Room(
        pygame.Rect(50, 330, 700, 220),
        pygame.Rect(520, 490, 150, 50),
        "Sleepingroom"
    )

    return {
        "room_1": room_1,
        "room_2": room_2
    }
