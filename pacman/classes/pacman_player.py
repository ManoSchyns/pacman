from collections.abc import Callable
from pathlib import Path
import pygame
from animation import Animation
from .movement import GridMovement
from .pacman import Pacman

ROOT = Path(__file__).resolve().parents[2]

SHEET_PATH = (
    ROOT / "sprietsheet" / "dbc1ie6-95c45f24-9ea6-462e-88bd-15f1a3d6e051.png"
)

KEY_DIRECTIONS: dict[int, str] = {
    pygame.K_RIGHT: "right",
    pygame.K_LEFT: "left",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
}


class PacmanPlayer:

    def __init__(self, position: tuple[int, int], size: int,
                 speed: float, cell_size: int,
                 is_open: Callable[[tuple[int, int], str], bool]) -> None:
        self.sprite = Pacman(str(SHEET_PATH), size)
        self.animations = {
            action: Animation(self.sprite.frames(action),
                              loop=action != "death")
            for action in self.sprite.actions()
        }

        self.movement: GridMovement = GridMovement(position, cell_size,
                                                   speed, is_open)
        self.animation = self.animations[self.movement.current_direction]
        self.rect = self.animation.current_frame().get_rect(center=position)

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        for key, direction in KEY_DIRECTIONS.items():
            if keys[key]:
                self.movement.request(direction)
                return

    def move(self, dt: float) -> None:
        previous = self.movement.current_direction
        self.rect.center = self.movement.update(dt)

        if self.movement.current_direction != previous:
            self.animation = self.animations[self.movement.current_direction]
            self.animation.reset()
        if self.movement.moving:
            self.animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(
            self.animation.current_frame(),
            self.rect
        )
