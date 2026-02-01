import pygame


class Avatar:
    def __init__(self, name, color, position, style):
        """
        style: "hair" oder "cap"
        """
        self.name = name
        self.color = color

        # ORIGINAL-POSITION
        self.base_x, self.y = position

        # FESTE VERSCHIEBUNG NACH RECHTS
        self.offset_x = 800  # <<<<<< HIER kannst du den Wert ändern

        self.style = style
        self.active = False

    def draw(self, screen, font):
        # === ENDGÜLTIGE POSITION ===
        x = self.base_x + self.offset_x
        y = self.y

        body_color = self.color if self.active else (130, 130, 130)
        head_pos = (x, y - 30)

        # === HAARE oder CAP ===
        if self.style == "hair":
            self._draw_hair(screen, head_pos)
        elif self.style == "cap":
            self._draw_cap(screen, head_pos)

        # === KOPF ===
        pygame.draw.circle(screen, (255, 220, 180), head_pos, 18)

        # === KÖRPER ===
        pygame.draw.rect(screen, body_color, (x - 15, y - 5, 30, 45))

        # === AKTIV-RING ===
        if self.active:
            pygame.draw.circle(screen, (0, 255, 0), head_pos, 22, 3)

        # === NAME ===
        label = font.render(self.name, True, (255, 255, 255))
        screen.blit(label, (x - label.get_width() // 2, y + 45))

    # ================= STYLES =================

    def _draw_hair(self, screen, head_pos):
        x, y = head_pos
        hair_color = (80, 40, 20)

        pygame.draw.circle(screen, hair_color, (x, y - 6), 20)
        pygame.draw.rect(screen, hair_color, (x - 20, y - 6, 40, 20))

    def _draw_cap(self, screen, head_pos):
        x, y = head_pos
        cap_color = (40, 40, 40)

        pygame.draw.arc(
            screen,
            cap_color,
            (x - 20, y - 20, 40, 40),
            3.14, 0,
            4
        )

        pygame.draw.rect(screen, cap_color, (x, y - 5, 18, 6))
