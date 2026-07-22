import math

import pygame
import pytweening

from animation import Animation
from .menu import BLUE, FONT_PATH, GREY, PALE_YELLOW, WHITE, YELLOW, blend

OVERLAY_ALPHA = 205
FADE_TIME = 0.28
TITLE_TIME = 0.45
ITEM_DELAY = 0.09
ITEM_TIME = 0.3
CURSOR_SIZE = 26


class PauseMenu:
    """Menu de pause affiché par-dessus la partie mise en attente."""

    ITEMS = ("RESUME", "MAIN MENU")

    def __init__(self, screen: pygame.Surface,
                 cursor_frames: list[pygame.Surface]) -> None:
        """Prépare les polices et le curseur Pacman du menu de pause."""
        self.screen = screen
        self.width, self.height = screen.get_size()

        self.title_font = pygame.font.Font(str(FONT_PATH), 54)
        self.item_font = pygame.font.Font(str(FONT_PATH), 26)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 13)

        self.cursor = Animation(
            [pygame.transform.scale(frame, (CURSOR_SIZE, CURSOR_SIZE))
             for frame in cursor_frames], 0.09)

        self.selected = 0
        self.item_rects: list[pygame.Rect] = []
        self.time = 0.0

    def run(self) -> str:
        """Affiche le menu de pause et attend le choix du joueur.

        Returns:
            "resume" pour reprendre, "menu" pour revenir au menu
            principal, "quit" si la fenêtre a été fermée.
        """
        background = self.screen.copy()
        clock: pygame.time.Clock = pygame.time.Clock()
        self.selected = 0
        self.time = 0.0

        result: str | None = None
        while result is None:
            dt = min(clock.tick(60) / 1000, 1 / 30)
            self.time += dt
            self.cursor.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = "quit"
                    break
                if event.type == pygame.KEYDOWN:
                    result = self._handle_key(event.key)
                    if result is not None:
                        break
                elif event.type == pygame.MOUSEMOTION:
                    self._hover(event.pos)
                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self._hover(event.pos):
                        result = self._activate()
                        break

            self._draw(background)
            pygame.display.flip()

        return result

    def _handle_key(self, key: int) -> str | None:
        """Traite une touche et retourne l'action choisie si besoin."""
        if key == pygame.K_ESCAPE:
            return "resume"
        if key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.ITEMS)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.ITEMS)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            return self._activate()
        return None

    def _hover(self, position: tuple[int, int]) -> bool:
        """Sélectionne l'entrée survolée et indique si la souris est dessus."""
        for index, rect in enumerate(self.item_rects):
            if rect.collidepoint(position):
                self.selected = index
                return True
        return False

    def _activate(self) -> str:
        """Retourne l'action correspondant à l'entrée sélectionnée."""
        if self.ITEMS[self.selected] == "RESUME":
            return "resume"
        return "menu"

    def _draw(self, background: pygame.Surface) -> None:
        """Dessine la partie figée, le voile, le titre et les entrées."""
        self.screen.blit(background, (0, 0))

        fade = pytweening.easeOutCubic(min(self.time / FADE_TIME, 1.0))
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((6, 6, 16, int(OVERLAY_ALPHA * fade)))
        self.screen.blit(overlay, (0, 0))

        self._draw_title()
        self._draw_items()

        pygame.draw.rect(self.screen, BLUE,
                         pygame.Rect(10, 10, self.width - 20,
                                     self.height - 20),
                         3, border_radius=14)

        hint = self.hint_font.render("ESC : RESUME", True, WHITE)
        hint.set_alpha(int(120 + 90 * math.sin(self.time * 3.2)))
        self.screen.blit(hint, hint.get_rect(
            center=(self.width // 2, int(self.height * 0.72))))

    def _draw_title(self) -> None:
        """Fait descendre le titre PAUSE avec un léger rebond."""
        progress = pytweening.easeOutBack(min(self.time / TITLE_TIME, 1.0))
        target_y = int(self.height * 0.33)
        y = int(-80 + (target_y + 80) * progress)

        pulse = 0.5 + 0.5 * math.sin(self.time * 2.6)
        title = self.title_font.render("PAUSE", True,
                                       blend(YELLOW, PALE_YELLOW, pulse))
        self.screen.blit(title, title.get_rect(
            center=(self.width // 2, y)))

    def _draw_items(self) -> None:
        """Fait apparaître les entrées en cascade et met en avant le choix."""
        self.item_rects = []
        base_y = int(self.height * 0.47)

        for index, label in enumerate(self.ITEMS):
            start = TITLE_TIME * 0.6 + index * ITEM_DELAY
            appear = min(max((self.time - start) / ITEM_TIME, 0.0), 1.0)
            eased = pytweening.easeOutCubic(appear)
            selected = index == self.selected

            if selected:
                pulse = 0.5 + 0.5 * math.sin(self.time * 5.0)
                color = blend(YELLOW, PALE_YELLOW, pulse)
            else:
                color = GREY

            text = self.item_font.render(label, True, color)
            text.set_alpha(int(255 * eased))
            offset = int((1 - eased) * 30)
            rect = text.get_rect(
                center=(self.width // 2, base_y + index * 62 + offset))
            self.item_rects.append(rect.inflate(70, 20))
            self.screen.blit(text, rect)

            if selected and eased > 0.9:
                frame = self.cursor.current_frame()
                self.screen.blit(frame, frame.get_rect(
                    midright=(rect.left - 24, rect.centery)))
