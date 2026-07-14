import math
import random
from dataclasses import dataclass
from pathlib import Path

import pygame
import pytweening

from ghost.classes import Blinky, Clyde, Ghost, Inky, Pinky
from pacman.animations import Animation
from pacman.classes.pacman import Pacman

ROOT = Path(__file__).resolve().parents[2]
TITLE_PATH = ROOT / "assets" / "pacman_title_transparent.png"
FONT_PATH = ROOT / "game" / "srcs" / "ARCADE_N.TTF"
SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)

YELLOW = (255, 222, 0)
PALE_YELLOW = (255, 255, 190)
WHITE = (222, 222, 222)
GREY = (120, 120, 135)
BLUE = (33, 33, 222)
DOT_COLOR = (255, 183, 174)
CYAN = (0, 255, 255)


def blend(first: tuple[int, int, int], second: tuple[int, int, int],
          amount: float) -> tuple[int, int, int]:
    return (int(first[0] + (second[0] - first[0]) * amount),
            int(first[1] + (second[1] - first[1]) * amount),
            int(first[2] + (second[2] - first[2]) * amount))


@dataclass
class ParadeGhost:
    chase: Animation
    frightened: Animation
    eaten: Animation
    x: float
    state: str


@dataclass
class ScorePopup:
    x: float
    y: float
    value: int
    age: float


class ChaseParade:

    HUNT_SPEED = 220.0
    FLEE_SPEED = 150.0
    CHASE_SPEED = 260.0
    EYES_SPEED = 540.0
    GAP = 54.0
    LEAD = 120.0
    SCORES = (200, 400, 800, 1600)
    POPUP_LIFE = 0.9

    def __init__(self, width: int, y: int, size: int,
                 pacman: Pacman, ghosts: list[Ghost]) -> None:
        self.width = width
        self.y = y
        self.size = size
        self.pac_left = Animation(pacman.frames("left"), 0.08)
        self.pac_right = Animation(pacman.frames("right"), 0.08)
        self.ghosts = [
            ParadeGhost(Animation(self._scaled(ghost, "left"), 0.12),
                        Animation(self._scaled(ghost, "frightened"), 0.12),
                        Animation(self._scaled(ghost, "eaten"), 0.2),
                        0.0, "chase")
            for ghost in ghosts
        ]
        self.popups: list[ScorePopup] = []
        self.pac_x = 0.0
        self.eaten = 0
        self.phase = "hunt"
        self.dots: list[int] = []
        self._start_hunt()

    def _scaled(self, ghost: Ghost, action: str) -> list[pygame.Surface]:
        return [pygame.transform.scale(frame, (self.size, self.size))
                for frame in ghost.frames(action)]

    def _start_hunt(self) -> None:
        self.phase = "hunt"
        self.pac_x = float(self.width + 60)
        self.dots = list(range(40, self.width - 30, 46))
        for index, ghost in enumerate(self.ghosts):
            ghost.state = "chase"
            ghost.x = self.pac_x + self.LEAD + index * self.GAP

    def _start_flee(self) -> None:
        self.phase = "flee"
        self.eaten = 0
        base = -4 * self.GAP - 60
        for index, ghost in enumerate(self.ghosts):
            ghost.state = "flee"
            ghost.x = base + index * self.GAP
        self.pac_x = base - self.LEAD

    def update(self, dt: float) -> None:
        self.pac_left.update(dt)
        self.pac_right.update(dt)
        for ghost in self.ghosts:
            ghost.chase.update(dt)
            ghost.frightened.update(dt)
            ghost.eaten.update(dt)

        if self.phase == "hunt":
            self.pac_x -= self.HUNT_SPEED * dt
            for index, ghost in enumerate(self.ghosts):
                ghost.x = self.pac_x + self.LEAD + index * self.GAP
            self.dots = [dot for dot in self.dots if dot < self.pac_x - 8]
            if self.ghosts[-1].x < -80:
                self._start_flee()
        else:
            self.pac_x += self.CHASE_SPEED * dt
            for ghost in self.ghosts:
                if ghost.state == "eaten":
                    ghost.x += self.EYES_SPEED * dt
                else:
                    ghost.x += self.FLEE_SPEED * dt
                    if ghost.x <= self.pac_x + self.size * 0.4:
                        ghost.state = "eaten"
                        score = self.SCORES[min(self.eaten, 3)]
                        self.popups.append(
                            ScorePopup(ghost.x, self.y - 34, score, 0.0))
                        self.eaten += 1
            if self.pac_x > self.width + 80:
                self._start_hunt()

        for popup in self.popups:
            popup.age += dt
        self.popups = [p for p in self.popups if p.age < self.POPUP_LIFE]

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        if self.phase == "hunt":
            for dot in self.dots:
                pygame.draw.circle(screen, DOT_COLOR, (dot, self.y), 3)

        half = self.size // 2
        for ghost in self.ghosts:
            if ghost.x < -self.size or ghost.x > self.width + self.size:
                continue
            if ghost.state == "chase":
                frame = ghost.chase.current_frame()
            elif ghost.state == "flee":
                frame = ghost.frightened.current_frame()
            else:
                frame = ghost.eaten.current_frame()
            screen.blit(frame, (int(ghost.x) - half, self.y - half))

        if self.phase == "hunt":
            pacman = self.pac_left.current_frame()
        else:
            pacman = self.pac_right.current_frame()
        if -self.size <= self.pac_x <= self.width + self.size:
            screen.blit(pacman, (int(self.pac_x) - half, self.y - half))

        for popup in self.popups:
            fade = 1.0 - popup.age / self.POPUP_LIFE
            text = font.render(str(popup.value), True, CYAN)
            text.set_alpha(int(255 * fade))
            rise = int(26 * pytweening.easeOutCubic(popup.age
                                                    / self.POPUP_LIFE))
            screen.blit(text, text.get_rect(
                center=(int(popup.x), int(popup.y) - rise)))


class MainMenu:

    ITEMS = ("START GAME", "HIGHSCORES", "INSTRUCTIONS", "EXIT")

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.width, self.height = screen.get_size()

        raw = pygame.image.load(str(TITLE_PATH)).convert_alpha()
        trimmed = raw.subsurface(raw.get_bounding_rect()).copy()
        scale = (self.width * 0.62) / trimmed.get_width()
        self.logo = pygame.transform.smoothscale_by(trimmed, scale)
        self.glow = pygame.transform.smoothscale_by(self.logo, 1.07)
        self.title_y = int(self.height * 0.19)

        self.item_font = pygame.font.Font(str(FONT_PATH), 26)
        self.page_title_font = pygame.font.Font(str(FONT_PATH), 34)
        self.page_font = pygame.font.Font(str(FONT_PATH), 18)
        self.hint_font = pygame.font.Font(str(FONT_PATH), 13)
        self.small_font = pygame.font.Font(str(FONT_PATH), 11)

        pacman = Pacman(str(SHEET_PATH), 36)
        ghosts: list[Ghost] = [Blinky(str(SHEET_PATH)),
                               Pinky(str(SHEET_PATH)),
                               Inky(str(SHEET_PATH)),
                               Clyde(str(SHEET_PATH))]
        self.parade = ChaseParade(self.width, int(self.height * 0.84),
                                  36, pacman, ghosts)
        self.cursor = Animation(
            [pygame.transform.scale(frame, (26, 26))
             for frame in pacman.frames("right")], 0.09)

        rng = random.Random(7)
        self.twinkles: list[tuple[int, int, float, int]] = []
        while len(self.twinkles) < 26:
            x = rng.randrange(50, self.width - 50)
            y = rng.randrange(50, self.height - 90)
            in_title = y < self.height * 0.32
            in_menu = (self.height * 0.38 < y < self.height * 0.72
                       and self.width * 0.2 < x < self.width * 0.8)
            in_parade = y > self.height * 0.78
            if in_title or in_menu or in_parade:
                continue
            radius = 5 if len(self.twinkles) % 4 == 0 else 3
            self.twinkles.append((x, y, rng.random(), radius))

        self.selected = 0
        self.item_rects: list[pygame.Rect] = []
        self.time = 0.0

    def run(self) -> str:
        clock: pygame.time.Clock = pygame.time.Clock()
        while True:
            dt = min(clock.tick(60) / 1000, 1 / 30)
            self.time += dt
            self.parade.update(dt)
            self.cursor.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    action = self._handle_key(event.key)
                    if action is not None:
                        return action
                elif event.type == pygame.MOUSEMOTION:
                    self._hover(event.pos)
                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self._hover(event.pos):
                        action = self._activate()
                        if action is not None:
                            return action

            self._draw()
            pygame.display.flip()

    def _handle_key(self, key: int) -> str | None:
        if key in (pygame.K_UP, pygame.K_w):
            self.selected = (self.selected - 1) % len(self.ITEMS)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.selected = (self.selected + 1) % len(self.ITEMS)
        elif key in (pygame.K_RETURN, pygame.K_SPACE):
            return self._activate()
        return None

    def _hover(self, position: tuple[int, int]) -> bool:
        for index, rect in enumerate(self.item_rects):
            if rect.collidepoint(position):
                self.selected = index
                return True
        return False

    def _activate(self) -> str | None:
        label = self.ITEMS[self.selected]
        if label == "START GAME":
            return "start"
        if label == "EXIT":
            return "quit"
        lines: tuple[str, ...]
        if label == "HIGHSCORES":
            lines = ("NO SCORES YET", "",
                     "PLAY A GAME TO SET", "THE FIRST RECORD !")
        else:
            lines = ("ARROW KEYS : MOVE", "ESC : PAUSE",
                     "SPACE : SKIP LEVEL", "",
                     "EAT ALL PACGUMS", "AVOID THE GHOSTS !")
        if not self._show_page(label, lines):
            return "quit"
        return None

    def _show_page(self, title: str, lines: tuple[str, ...]) -> bool:
        clock: pygame.time.Clock = pygame.time.Clock()
        back_keys = (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_BACKSPACE)
        while True:
            dt = min(clock.tick(60) / 1000, 1 / 30)
            self.time += dt
            self.parade.update(dt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key in back_keys:
                    return True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True

            self._draw_background()
            heading = self.page_title_font.render(title, True, YELLOW)
            self.screen.blit(heading, heading.get_rect(
                center=(self.width // 2, int(self.height * 0.18))))

            y = int(self.height * 0.36)
            for line in lines:
                if line:
                    text = self.page_font.render(line, True, WHITE)
                    self.screen.blit(text, text.get_rect(
                        center=(self.width // 2, y)))
                y += 48

            blink = int(150 + 105 * math.sin(self.time * 3.2))
            back = self.hint_font.render("ESC : BACK", True, WHITE)
            back.set_alpha(blink)
            self.screen.blit(back, back.get_rect(
                center=(self.width // 2, int(self.height * 0.7))))
            pygame.display.flip()

    def _draw(self) -> None:
        self._draw_background()
        self._draw_title()
        self._draw_items()

        if self.time > 1.6:
            blink = int(140 + 90 * math.sin(self.time * 3.2))
            hint = self.hint_font.render(
                "ARROWS : NAVIGATE    ENTER : SELECT", True, WHITE)
            hint.set_alpha(blink)
            self.screen.blit(hint, hint.get_rect(
                center=(self.width // 2, int(self.height * 0.73))))

        credit = self.small_font.render("42 EDITION", True, GREY)
        self.screen.blit(credit, credit.get_rect(
            center=(self.width // 2, self.height - 36)))

    def _draw_background(self) -> None:
        self.screen.fill((0, 0, 0))
        for x, y, phase, radius in self.twinkles:
            progress = (self.time * 0.45 + phase) % 1.0
            wave = pytweening.easeInOutSine(1 - abs(1 - 2 * progress))
            color = blend((60, 42, 40), DOT_COLOR, 0.15 + 0.85 * wave)
            pygame.draw.circle(self.screen, color, (x, y), radius)

        self.parade.draw(self.screen, self.hint_font)
        pygame.draw.rect(self.screen, BLUE,
                         pygame.Rect(10, 10, self.width - 20,
                                     self.height - 20),
                         3, border_radius=14)
        pygame.draw.rect(self.screen, BLUE,
                         pygame.Rect(18, 18, self.width - 36,
                                     self.height - 36),
                         3, border_radius=10)

    def _draw_title(self) -> None:
        progress = pytweening.easeOutBounce(min(self.time / 1.15, 1.0))
        start_y = -self.logo.get_height()
        y = start_y + (self.title_y - start_y) * progress
        settle = max(0.0, min((self.time - 1.15) / 0.9, 1.0))
        bob = math.sin(self.time * 2.1) * 7 * settle

        rect = self.logo.get_rect(
            center=(self.width // 2, int(y + bob)))
        pulse = 0.5 + 0.5 * math.sin(self.time * 2.6)
        self.glow.set_alpha(int(40 + 55 * pulse * settle))
        self.screen.blit(self.glow, self.glow.get_rect(center=rect.center))
        self.screen.blit(self.logo, rect)

    def _draw_items(self) -> None:
        self.item_rects = []
        base_y = int(self.height * 0.435)
        for index, label in enumerate(self.ITEMS):
            appear = min(max((self.time - 0.85 - index * 0.13) / 0.4, 0.0),
                         1.0)
            eased = pytweening.easeOutCubic(appear)
            selected = index == self.selected

            if selected:
                pulse = 0.5 + 0.5 * math.sin(self.time * 5.0)
                color = blend(YELLOW, PALE_YELLOW, pulse)
            else:
                color = GREY
            text = self.item_font.render(label, True, color)
            text.set_alpha(int(255 * eased))
            offset = int((1 - eased) * 36)
            rect = text.get_rect(
                center=(self.width // 2, base_y + index * 64 + offset))
            self.item_rects.append(rect.inflate(70, 20))
            self.screen.blit(text, rect)

            if selected and eased > 0.9:
                frame = self.cursor.current_frame()
                self.screen.blit(frame, frame.get_rect(
                    midright=(rect.left - 24, rect.centery)))
