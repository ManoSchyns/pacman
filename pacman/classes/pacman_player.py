import sys
from pathlib import Path
import pygame
from pacman.animations import Animation
from .pacman import Pacman

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "sprietsheet"))

SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)


class PacmanPlayer:

    def __init__(self, position: tuple[int, int], size: int) -> None:
        self.speed = (0, 2)

        self.sprite = Pacman(SHEET_PATH, size)
        self.animations = {
            action: Animation(self.sprite.frames(action))
            for action in self.sprite.actions()
        }

        self.direction = "down"
        self.prev_direction = "down"
        self.animation = self.animations[self.direction]

        self.rect = self.animation.current_frame().get_rect(center=position)

    def set_direction(self, direction: str) -> None:
        if self.direction != direction:
            self.direction = direction
            self.animation = self.animations[direction]
            self.animation.reset()

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.prev_direction = self.direction
            self.set_direction("right")

        elif keys[pygame.K_LEFT]:
            self.prev_direction = self.direction
            self.set_direction("left")

        elif keys[pygame.K_UP]:
            self.prev_direction = self.direction
            self.set_direction("up")

        elif keys[pygame.K_DOWN]:
            self.prev_direction = self.direction
            self.set_direction("down")

    def move(self, dt: float) -> None:
        self.animation.update(dt)

        if self.direction == "right":
            self.speed = (2, 0)

        elif self.direction == "left":
            self.speed = (-2, 0)

        elif self.direction == "up":
            self.speed = (0, -2)

        elif self.direction == "down":
            self.speed = (0, 2)
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def go_back(self) -> None:
        self.rect.x -= self.speed[0]
        self.rect.y -= self.speed[1]
        self.set_direction(self.prev_direction)

    def draw(self, screen) -> None:
        screen.blit(
            self.animation.current_frame(),
            self.rect
        )
