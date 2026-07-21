from collections.abc import Callable
import pygame

DIRECTIONS: dict[str, tuple[int, int]] = {
    "right": (1, 0),
    "left": (-1, 0),
    "up": (0, -1),
    "down": (0, 1),
}

OPPOSITES: dict[str, str] = {
    "right": "left",
    "left": "right",
    "up": "down",
    "down": "up",
}

TURN_TOLERANCE_RATIO = 0.25
EPS = 1e-6


class GridMovement:
    """Moteur de déplacement sur grille.

    La direction demandée par le joueur est mémorisée dans
    wanted_direction et n'est appliquée qu'au centre d'une case, avec
    une tolérance, pour ne pas rester bloqué dans les virages.
    """

    def __init__(self, position: tuple[int, int], cell_size: int,
                 speed: float,
                 is_open: Callable[[tuple[int, int], str], bool],
                 direction: str = "down") -> None:
        """Initialise la position, la vitesse et la direction de départ.

        Args:
            position: position de départ en pixels.
            cell_size: taille d'une case en pixels.
            speed: vitesse de déplacement en pixels par seconde.
            is_open: fonction indiquant si une case est ouverte vers
                une direction.
            direction: direction initiale.
        """
        self.x: float = float(position[0])
        self.y: float = float(position[1])
        self.cell_size = cell_size
        self.speed = speed
        self.normal_speed = speed
        self.is_open = is_open
        self.tolerance = cell_size * TURN_TOLERANCE_RATIO
        self.current_direction = direction
        self.wanted_direction = direction
        self.moving = True

        self.dead_cooldown = 1
        self.dead_cooldown_start = pygame.time.get_ticks()

    def can_move(self) -> bool:
        """Retourne True si le délai d'attente initial est écoulé."""
        curr = pygame.time.get_ticks()
        elapsed = curr - self.dead_cooldown_start

        if elapsed // 1000 >= self.dead_cooldown:
            return True
        return False

    def request(self, direction: str) -> None:
        """Mémorise la direction demandée pour le prochain virage."""
        self.wanted_direction = direction

    def position(self) -> tuple[int, int]:
        """Retourne la position courante arrondie en pixels."""
        return (round(self.x), round(self.y))

    def cell(self) -> tuple[int, int]:
        """Retourne la case de la grille actuellement occupée."""
        return (int(self.x // self.cell_size),
                int(self.y // self.cell_size))

    def at_decision_point(self) -> bool:
        """Retourne True si on est assez proche du centre de la case."""
        center = self._center(self.cell())
        return (abs(center[0] - self.x) <= self.tolerance
                and abs(center[1] - self.y) <= self.tolerance)

    def update(self, dt: float) -> tuple[int, int]:
        """Applique le virage en attente puis avance d'un pas.

        Args:
            dt: temps écoulé depuis la frame précédente, en secondes.

        Returns:
            La nouvelle position en pixels.
        """
        if self.can_move():
            dt = min(dt, 1 / 30)
            self._try_turn()
            if self.moving:
                self._advance(self.speed * dt)
        return self.position()

    def _try_turn(self) -> None:
        """Applique la direction demandée si elle est possible.

        Le demi-tour est immédiat, les autres virages ne sont pris
        qu'à portée du centre de la case et si le passage est ouvert.
        """
        wanted = self.wanted_direction
        current = self.current_direction
        if wanted == current:
            return

        if not self.moving:
            if self.is_open(self.cell(), wanted):
                self.current_direction = wanted
                self.moving = True
            return

        if wanted == OPPOSITES[current]:
            self.current_direction = wanted
            return

        cell = self.cell()
        center = self._center(cell)
        if (abs(self._signed_distance(center, current)) <= self.tolerance
                and self.is_open(cell, wanted)):
            self.x, self.y = center
            self.current_direction = wanted

    def _advance(self, step: float) -> None:
        """Avance case par case et s'arrête net devant un mur.

        Args:
            step: distance à parcourir en pixels.
        """
        remaining = step
        while remaining > EPS:
            cell = self.cell()
            center = self._center(cell)
            distance = self._signed_distance(center, self.current_direction)

            if distance > EPS:
                travel = min(remaining, distance)
                self._move(travel)
                remaining -= travel
                if remaining > EPS and not self.is_open(
                        cell, self.current_direction):
                    self.x, self.y = center
                    self.moving = False
                    return
            else:
                if not self.is_open(cell, self.current_direction):
                    self.x, self.y = center
                    self.moving = False
                    return
                travel = min(remaining, self.cell_size + distance)
                self._move(travel)
                remaining -= travel

    def _move(self, distance: float) -> None:
        """Décale la position de la distance donnée."""
        offset_x, offset_y = DIRECTIONS[self.current_direction]
        self.x += offset_x * distance
        self.y += offset_y * distance

    def _center(self, cell: tuple[int, int]) -> tuple[float, float]:
        """Retourne les coordonnées du centre de la case donnée."""
        return (cell[0] * self.cell_size + self.cell_size / 2,
                cell[1] * self.cell_size + self.cell_size / 2)

    def _signed_distance(self, target: tuple[float, float],
                         direction: str) -> float:
        """Retourne la distance jusqu'à la cible le long d'une direction.

        Args:
            target: point visé en pixels.
            direction: direction servant d'axe de projection.

        Returns:
            Une distance positive si la cible est devant, négative
            sinon.
        """
        offset_x, offset_y = DIRECTIONS[direction]
        return ((target[0] - self.x) * offset_x
                + (target[1] - self.y) * offset_y)
