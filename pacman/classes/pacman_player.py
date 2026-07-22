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
    """Pacman contrôlé par le joueur, avec ses animations."""

    def __init__(self, position: tuple[int, int], size: int,
                 speed: float, cell_size: int,
                 is_open: Callable[[tuple[int, int], str], bool]) -> None:
        """Charge les animations et prépare le moteur de déplacement.

        Args:
            position: position de départ en pixels.
            size: taille du sprite en pixels.
            speed: vitesse de déplacement en pixels par seconde.
            cell_size: taille d'une case en pixels.
            is_open: fonction indiquant si une case est ouverte vers
                une direction.
        """
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
        """Lit les flèches du clavier et demande la direction voulue."""
        keys = pygame.key.get_pressed()
        for key, direction in KEY_DIRECTIONS.items():
            if keys[key]:
                self.movement.request(direction)
                return

    def move(self, dt: float) -> None:
        """Déplace Pacman et met à jour l'animation de sa direction.

        Args:
            dt: temps écoulé depuis la frame précédente, en secondes.
        """
        previous = self.movement.current_direction
        self.rect.center = self.movement.update(dt)

        if self.movement.current_direction != previous:
            self.animation = self.animations[self.movement.current_direction]
            self.animation.reset()
        if self.movement.moving:
            self.animation.update(dt)

    def draw(self, screen: pygame.Surface) -> None:
        """Dessine la frame courante de Pacman sur l'écran."""
        screen.blit(
            self.animation.current_frame(),
            self.rect
        )
