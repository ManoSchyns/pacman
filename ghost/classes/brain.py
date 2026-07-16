import random
from collections.abc import Callable
from dataclasses import dataclass
from pacman.classes.movement import DIRECTIONS, OPPOSITES

RANDOM_TURN_CHANCE = 0.2


@dataclass
class ChaseContext:
    fear: bool
    pacman_cell: tuple[int, int]
    pacman_direction: str
    blinky_cell: tuple[int, int]
    ghost_cell: tuple[int, int] = (0, 0)


class GhostBrain:

    def __init__(self,
                 random_turn_chance: float = RANDOM_TURN_CHANCE) -> None:
        self.random_turn_chance = random_turn_chance
        self.last_decision_cell: tuple[int, int] | None = None

    def target(self, context: ChaseContext) -> tuple[int, int]:
        return context.pacman_cell

    def choose(self, context: ChaseContext,
               cell: tuple[int, int], current_direction: str,
               is_open: Callable[[tuple[int, int], str], bool],
               target_cell: tuple[int, int],
               force: bool = False) -> str | None:
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
            return max(options, key=lambda direction: self._distance(
             cell, direction, context.pacman_cell))

        return min(options, key=lambda direction: self._distance(
            cell, direction, target_cell))

    @staticmethod
    def _distance(cell: tuple[int, int], direction: str,
                  target_cell: tuple[int, int]) -> int:
        offset_x, offset_y = DIRECTIONS[direction]
        next_x = cell[0] + offset_x
        next_y = cell[1] + offset_y
        return ((next_x - target_cell[0]) ** 2
                + (next_y - target_cell[1]) ** 2)


class AmbushBrain(GhostBrain):

    LOOKAHEAD = 4

    def target(self, context: ChaseContext) -> tuple[int, int]:
        offset_x, offset_y = DIRECTIONS[context.pacman_direction]
        return (context.pacman_cell[0] + offset_x * self.LOOKAHEAD,
                context.pacman_cell[1] + offset_y * self.LOOKAHEAD)


class CowardBrain(GhostBrain):

    NEAR_DISTANCE = 8

    def __init__(self, corner_cell: tuple[int, int],
                 random_turn_chance: float = RANDOM_TURN_CHANCE) -> None:
        super().__init__(random_turn_chance)
        self.corner_cell = corner_cell

    def target(self, context: ChaseContext) -> tuple[int, int]:
        gap_x = context.ghost_cell[0] - context.pacman_cell[0]
        gap_y = context.ghost_cell[1] - context.pacman_cell[1]
        if gap_x ** 2 + gap_y ** 2 > self.NEAR_DISTANCE ** 2:
            return context.pacman_cell
        return self.corner_cell


class FlankBrain(GhostBrain):

    PIVOT_LOOKAHEAD = 2
    NEAR_DISTANCE = 8

    def target(self, context: ChaseContext) -> tuple[int, int]:
        gap_x = context.ghost_cell[0] - context.pacman_cell[0]
        gap_y = context.ghost_cell[1] - context.pacman_cell[1]
        if gap_x ** 2 + gap_y ** 2 > self.NEAR_DISTANCE ** 2:
            return context.pacman_cell

        offset_x, offset_y = DIRECTIONS[context.pacman_direction]
        pivot_x = context.pacman_cell[0] + offset_x * self.PIVOT_LOOKAHEAD
        pivot_y = context.pacman_cell[1] + offset_y * self.PIVOT_LOOKAHEAD
        return (2 * pivot_x - context.blinky_cell[0],
                2 * pivot_y - context.blinky_cell[1])
