import pygame


class Avatar:
    def __init__(self, name, color, position, style):
        """
        style: "hair" oder "cap"
        """
        self.name = name
        self.color = color
        self.x, self.y = position
        self.style = style
        self.active = False

    def draw(self, screen, font, offset_x=100):
        x = self.x +offset_x
        y = self.y

        body_color = self.color if self.active else (130, 130, 130)
        head_pos = (self.x, self.y - 30)

        # === HAARE oder CAP ===
        if self.style == "hair":
            self._draw_hair(screen, head_pos)

        elif self.style == "cap":
            self._draw_cap(screen, head_pos)

        # === KOPF ===
        pygame.draw.circle(screen, (255, 220, 180), head_pos, 18)

        # === KÖRPER ===
        pygame.draw.rect(screen, body_color, (self.x - 15, self.y - 5, 30, 45))

        # === AKTIV-RING ===
        if self.active:
            pygame.draw.circle(screen, (0, 255, 0), head_pos, 22, 3)

        # === NAME ===
        label = font.render(self.name, True, (255, 255, 255))
        screen.blit(label, (self.x - label.get_width() // 2, self.y + 45))

    # ================= STYLES =================

    def _draw_hair(self, screen, head_pos):
        """Offene Haare"""
        x, y = head_pos
        hair_color = (80, 40, 20)

        pygame.draw.circle(screen, hair_color, (x, y - 6), 20)
        pygame.draw.rect(screen, hair_color, (x - 20, y - 6, 40, 20))

    def _draw_cap(self, screen, head_pos):
        """Cap"""
        x, y = head_pos
        cap_color = (40, 40, 40)

        # Cap-Kuppel
        pygame.draw.arc(
            screen,
            cap_color,
            (x - 20, y - 20, 40, 40),
            3.14, 0,
            4
        )

        # Schirm
        pygame.draw.rect(screen, cap_color, (x, y - 5, 18, 6))
