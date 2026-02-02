# Erstellt von Jannik Langhammer
# Erzeugen des Raumes



import pygame
import config as config

# RAUM-KLASSE
class Room:
    def __init__(self, rect, window_rect, name):
        self.rect = rect
        self.window = window_rect
        self.rollo_height = 0   # Prozent (100 = komplett geschlossen)
        self.name = name
        self.light_level = 0  # Prozent (100 = voll an)
    
    def draw(self, surface, font):
    
        # Lichtsteuerung
        factor = self.light_level / 100  # 0.0 – 1.0

        floor_color = (
            int(config.FLOOR[0] * factor),
            int(config.FLOOR[1] * factor),
            int(config.FLOOR[2] * factor),
            )
        pygame.draw.rect(surface, floor_color, self.rect)
        pygame.draw.rect(surface, config.WALL, self.rect, 4)
        pygame.draw.rect(surface, config.WINDOW_COLOR, self.window)


        # Lichthelligkeit anzeigen
        light_text = font.render(
            f"Licht: {self.light_level}%",
            True,
            (255, 0, 0)
        )
        surface.blit(
            light_text,
            (self.rect.right - light_text.get_width() - 10, self.rect.y + 10)
        )

        # Rollosteuerung
        rollo_rect = pygame.Rect(
            self.window.x,
            self.window.y,
            self.window.width,
            self.rollo_height
        )
        # Rollohöhe anzeigen
        pygame.draw.rect(surface, config.ROLLO, rollo_rect)
        percent = int((self.rollo_height / self.window.height) * 100)

        percent_text = font.render(
            f"{percent}%",
            True,
            (255, 0, 0)
        )

        text_x = self.window.right + 10
        text_y = self.window.y + self.window.height // 2 - percent_text.get_height() // 2

        surface.blit(percent_text, (text_x, text_y))




# RÄUME ERZEUGEN


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
