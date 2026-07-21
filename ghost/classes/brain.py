import random
from collections.abc import Callable
from dataclasses import dataclass
from pacman.classes.movement import DIRECTIONS, OPPOSITES

RANDOM_TURN_CHANCE = 0.2


@dataclass
class ChaseContext:
    """Regroupe les informations de jeu utiles aux IA des fantômes."""

    fear: bool
    pacman_cell: tuple[int, int]
    pacman_direction: str
    blinky_cell: tuple[int, int]
    ghost_cell: tuple[int, int] = (0, 0)


class GhostBrain:
    """IA de base qui poursuit Pacman en ligne droite comme Blinky."""

    def __init__(self,
                 random_turn_chance: float = RANDOM_TURN_CHANCE) -> None:
        """Initialise l'IA avec sa probabilité de virage aléatoire."""
        self.random_turn_chance = random_turn_chance
        self.last_decision_cell: tuple[int, int] | None = None

    def target(self, context: ChaseContext) -> tuple[int, int]:
        """Retourne la case visée, ici la position de Pacman."""
        return context.pacman_cell

    def choose(self, context: ChaseContext,
               cell: tuple[int, int], current_direction: str,
               is_open: Callable[[tuple[int, int], str], bool],
               target_cell: tuple[int, int],
               force: bool = False) -> str | None:
        """Choisit la direction à prendre depuis la case courante.

        Args:
            context: état du jeu utilisé pour connaître la peur.
            cell: case actuelle du fantôme.
            current_direction: direction suivie actuellement.
            is_open: test indiquant si une direction est praticable.
            target_cell: case que le fantôme cherche à atteindre.
            force: force une nouvelle décision sur la même case.

        Returns:
            La direction retenue, ou None si aucune décision n'est prise.
        """
        if not force and cell == self.last_decision_cell:
            return None
        self.last_decision_cell = cell

        options = [direction for direction in DIRECTIONS
                   if direction != OPPOSITES[current_direction]
                   and is_open(cell, direction)]

        if not options:
            back = OPPOSITES[current_direction]
            if is_open(cell, back):
                return back
            return None

        if random.random() < self.random_turn_chance:
            return random.choice(options)

        if context.fear:
            opp = OPPOSITES[current_direction]
            if is_open(cell, opp) and self.can_revert(context, cell):
                options.append(opp)
            return max(options, key=lambda direction: self._distance(
             cell, direction, context.pacman_cell))

        return min(options, key=lambda direction: self._distance(
            cell, direction, target_cell))

    def can_revert(self, context: ChaseContext, cell: tuple[int, int]) -> bool:
        """Vérifie si le fantôme est aligné avec Pacman."""
        same_line = cell[1] == context.pacman_cell[1]
        same_col = cell[0] == context.pacman_cell[0]

        if same_line or same_col:
            return True

        return False

    @staticmethod
    def _distance(cell: tuple[int, int], direction: str,
                  target_cell: tuple[int, int]) -> int:
        """Calcule la distance au carré entre la case suivante et la cible."""
        offset_x, offset_y = DIRECTIONS[direction]
        next_x = cell[0] + offset_x
        next_y = cell[1] + offset_y
        return ((next_x - target_cell[0]) ** 2
                + (next_y - target_cell[1]) ** 2)


class AmbushBrain(GhostBrain):
    """IA de Pinky qui tend une embuscade devant Pacman."""

    LOOKAHEAD = 4

    def target(self, context: ChaseContext) -> tuple[int, int]:
        """Retourne la case située quelques cases devant Pacman."""
        offset_x, offset_y = DIRECTIONS[context.pacman_direction]
        return (context.pacman_cell[0] + offset_x * self.LOOKAHEAD,
                context.pacman_cell[1] + offset_y * self.LOOKAHEAD)


class CowardBrain(GhostBrain):
    """IA de Clyde qui fuit vers son coin dès qu'il approche Pacman."""

    NEAR_DISTANCE = 8

    def __init__(self, corner_cell: tuple[int, int],
                 random_turn_chance: float = RANDOM_TURN_CHANCE) -> None:
        """Initialise l'IA avec le coin de repli du fantôme."""
        super().__init__(random_turn_chance)
        self.corner_cell = corner_cell

    def target(self, context: ChaseContext) -> tuple[int, int]:
        """Retourne Pacman si loin, sinon le coin de repli."""
        gap_x = context.ghost_cell[0] - context.pacman_cell[0]
        gap_y = context.ghost_cell[1] - context.pacman_cell[1]
        if gap_x ** 2 + gap_y ** 2 > self.NEAR_DISTANCE ** 2:
            return context.pacman_cell
        return self.corner_cell


class FlankBrain(GhostBrain):
    """IA d'Inky qui prend Pacman à revers en s'appuyant sur Blinky."""

    PIVOT_LOOKAHEAD = 2
    NEAR_DISTANCE = 8

    def target(self, context: ChaseContext) -> tuple[int, int]:
        """Retourne Pacman si loin, sinon la case symétrique de Blinky.

        Returns:
            La case obtenue en doublant le vecteur allant de Blinky
            au pivot placé devant Pacman.
        """
        gap_x = context.ghost_cell[0] - context.pacman_cell[0]
        gap_y = context.ghost_cell[1] - context.pacman_cell[1]
        if gap_x ** 2 + gap_y ** 2 > self.NEAR_DISTANCE ** 2:
            return context.pacman_cell

        offset_x, offset_y = DIRECTIONS[context.pacman_direction]
        pivot_x = context.pacman_cell[0] + offset_x * self.PIVOT_LOOKAHEAD
        pivot_y = context.pacman_cell[1] + offset_y * self.PIVOT_LOOKAHEAD
        return (2 * pivot_x - context.blinky_cell[0],
                2 * pivot_y - context.blinky_cell[1])
